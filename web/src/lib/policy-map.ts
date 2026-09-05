import ELK from 'elkjs/lib/elk.bundled.js';
import type { ElkNode } from 'elkjs/lib/elk-api';
import type { PublicData, Relationship } from './types';
import type {
  PolicyMapAtlas,
  PolicyMapEdge,
  PolicyMapLayout,
  PolicyMapMode,
  PolicyMapModel,
  PolicyMapNode,
  PolicyMapNodeKind,
  PolicyMapView,
} from './policy-map-types';

const elk = new ELK();
const graphId = (kind: string, entityId: string): string => `${kind}:${entityId}`;

export function readablePolicyMapLabel(value: string): string {
  const readable = value.replaceAll('_', ' ');
  return `${readable.charAt(0).toLocaleUpperCase('en-GB')}${readable.slice(1)}`;
}

export function wrapPolicyMapLabel(label: string): string[] {
  const lines: string[] = [];
  for (const word of label.trim().split(/\s+/)) {
    const current = lines.at(-1);
    if (current === undefined || `${current} ${word}`.length > 26) lines.push(word);
    else lines[lines.length - 1] = `${current} ${word}`;
  }
  return lines;
}

function endpointKind(value: string): PolicyMapNodeKind {
  if (value === 'document' || value === 'policy') return value;
  throw new Error(`Unsupported policy map endpoint type: ${value}`);
}

export function createPolicyMapModel(data: PublicData, base: string): PolicyMapModel {
  const prefix = base.endsWith('/') ? base : base + '/';
  const documents = new Map(data.documents.map((item) => [item.id, item]));
  const policies = new Map(data.policies.map((item) => [item.id, item]));
  const sources = new Map(data.sources.map((item) => [item.id, item]));
  const keys = new Set(data.relationships.flatMap((edge) => [
    graphId(edge.source_entity_type, edge.source_entity_id),
    graphId(edge.target_entity_type, edge.target_entity_id),
  ]));
  const nodes: PolicyMapNode[] = [];

  for (const key of keys) {
    const split = key.indexOf(':');
    const kind = endpointKind(key.slice(0, split));
    const entityId = key.slice(split + 1);
    if (kind === 'document') {
      const item = documents.get(entityId);
      if (!item) throw new Error(`Unresolved policy map endpoint: document:${entityId}`);
      nodes.push({
        id: key,
        entityId,
        kind,
        title: item.short_title,
        date: item.document_date,
        level: item.record_level,
        stage: item.corpus_assessment?.policy_stage ?? 'unclassified',
        policyIds: item.policies.map((policy) => policy.id),
        href: `${prefix}corpus/${item.slug}/`,
      });
    } else {
      const item = policies.get(entityId);
      if (!item) throw new Error(`Unresolved policy map endpoint: policy:${entityId}`);
      nodes.push({
        id: key,
        entityId,
        kind,
        title: item.short_name,
        date: '',
        level: 'principal',
        stage: 'policy',
        policyIds: [entityId],
        href: `${prefix}policies/${entityId}/`,
      });
    }
  }
  nodes.sort((a, b) => a.date.localeCompare(b.date) || a.id.localeCompare(b.id));

  const ids = new Set(nodes.map((node) => node.id));
  const edges = data.relationships.map((edge) => projectEdge(edge, ids, sources));
  return {
    nodes,
    edges,
    policies: data.policies.map((policy) => ({
      id: policy.id,
      title: policy.short_name,
      description: policy.scope_note,
    })),
    generatedAt: data.generated_at,
  };
}

function projectEdge(
  edge: Relationship,
  nodeIds: Set<string>,
  sources: Map<string, PublicData['sources'][number]>,
): PolicyMapEdge {
  const sourceKind = endpointKind(edge.source_entity_type);
  const targetKind = endpointKind(edge.target_entity_type);
  const source = graphId(sourceKind, edge.source_entity_id);
  const target = graphId(targetKind, edge.target_entity_id);
  if (!nodeIds.has(source) || !nodeIds.has(target)) {
    throw new Error(`Unresolved policy map endpoint for relationship: ${edge.id}`);
  }
  const evidence = edge.evidence_source_id === null ? undefined : sources.get(edge.evidence_source_id);
  return {
    id: edge.id,
    source,
    target,
    sourceEntityId: edge.source_entity_id,
    targetEntityId: edge.target_entity_id,
    sourceKind,
    targetKind,
    type: edge.relationship_type,
    basis: edge.basis,
    rationale: edge.rationale,
    evidence: evidence ? { url: evidence.url, publisher: evidence.publisher } : null,
  };
}

export function selectPolicyMapView(
  model: PolicyMapModel,
  family: string,
  mode: PolicyMapMode,
): PolicyMapView {
  const eligible = new Set(model.nodes
    .filter((node) => mode === 'all' || node.level === 'principal')
    .map((node) => node.id));
  const members = new Set(model.nodes
    .filter((node) => node.policyIds.includes(family) && eligible.has(node.id))
    .map((node) => node.id));
  const edges = model.edges.filter((edge) => (
    eligible.has(edge.source)
    && eligible.has(edge.target)
    && (mode === 'principal'
      ? members.has(edge.source) && members.has(edge.target)
      : members.has(edge.source) || members.has(edge.target))
  ));
  const visible = new Set([...members, ...edges.flatMap((edge) => [edge.source, edge.target])]);
  const nodes = model.nodes
    .filter((node) => visible.has(node.id))
    .map((node) => ({ ...node, context: !members.has(node.id) }));
  return {
    family,
    mode,
    nodes,
    edges,
    memberCount: members.size,
    contextCount: nodes.length - members.size,
    hidden: model.nodes.filter((node) => node.policyIds.includes(family)).length - members.size,
  };
}

async function arrange(view: PolicyMapView): Promise<PolicyMapLayout> {
  const definitions = new Map(view.nodes.map((node) => [node.id, node]));
  const reversed = new Set(view.edges.filter((edge) => {
    const source = definitions.get(edge.source);
    const target = definitions.get(edge.target);
    if (!source || !target) throw new Error(`Missing layout endpoint: ${edge.id}`);
    return source.date > target.date || (source.date === target.date && source.id > target.id);
  }).map((edge) => edge.id));
  const input: ElkNode = {
    id: 'root',
    layoutOptions: {
      'elk.algorithm': 'layered',
      'elk.direction': 'RIGHT',
      'elk.edgeRouting': 'ORTHOGONAL',
      'elk.randomSeed': '42',
      'elk.spacing.nodeNode': '36',
      'elk.spacing.componentComponent': '48',
      'elk.layered.spacing.nodeNodeBetweenLayers': '86',
      'elk.layered.considerModelOrder.strategy': 'NODES_AND_EDGES',
      'elk.padding': '[top=32,left=32,bottom=32,right=32]',
    },
    children: view.nodes.map((node) => ({
      id: node.id,
      width: 232,
      height: 58 + wrapPolicyMapLabel(node.title).length * 20,
    })),
    edges: view.edges.map((edge) => ({
      id: edge.id,
      sources: [reversed.has(edge.id) ? edge.target : edge.source],
      targets: [reversed.has(edge.id) ? edge.source : edge.target],
    })),
  };
  const graph = await elk.layout(input);
  const geometry = new Map((graph.children ?? []).map((node) => [node.id, node]));
  const routes = new Map((graph.edges ?? []).map((edge) => [edge.id, edge]));
  return {
    ...view,
    width: graph.width ?? 0,
    height: graph.height ?? 0,
    nodes: view.nodes.map((node) => {
      const placed = geometry.get(node.id);
      if (placed?.x === undefined || placed.y === undefined
        || placed.width === undefined || placed.height === undefined) {
        throw new Error(`Missing node geometry: ${node.id}`);
      }
      return {
        ...node,
        x: placed.x,
        y: placed.y,
        width: placed.width,
        height: placed.height,
        lines: wrapPolicyMapLabel(node.title),
      };
    }),
    edges: view.edges.map((edge) => {
      const section = routes.get(edge.id)?.sections?.[0];
      if (!section) throw new Error(`Missing edge route: ${edge.id}`);
      const points = [section.startPoint, ...(section.bendPoints ?? []), section.endPoint];
      return { ...edge, points: reversed.has(edge.id) ? points.reverse() : points };
    }),
  };
}

export async function buildPolicyMapAtlas(data: PublicData, base: string): Promise<PolicyMapAtlas> {
  const model = createPolicyMapModel(data, base);
  const views: Record<string, PolicyMapLayout> = {};
  const neighborhoods: Record<string, PolicyMapLayout> = {};
  for (const policy of model.policies) {
    for (const mode of ['principal', 'all'] as const) {
      views[`${policy.id}:${mode}`] = await arrange(selectPolicyMapView(model, policy.id, mode));
    }
  }
  for (const node of model.nodes) {
    const edges = model.edges.filter((edge) => edge.source === node.id || edge.target === node.id);
    const ids = new Set([node.id, ...edges.flatMap((edge) => [edge.source, edge.target])]);
    const nodes = model.nodes
      .filter((item) => ids.has(item.id))
      .map((item) => ({ ...item, context: item.id !== node.id }));
    neighborhoods[node.id] = await arrange({
      family: node.policyIds[0] ?? '',
      mode: 'all',
      nodes,
      edges,
      memberCount: 1,
      contextCount: nodes.length - 1,
      hidden: model.nodes.length - nodes.length,
    });
  }
  return { model, views, neighborhoods };
}

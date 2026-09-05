import assert from 'node:assert/strict';
import test from 'node:test';

import { loadPublicData } from '../src/lib/data.ts';
import { buildPolicyMapAtlas, createPolicyMapModel, relationshipTypeLabel, selectPolicyMapView, wrapPolicyMapLabel } from '../src/lib/policy-map.ts';

const data = loadPublicData();
const family = 'artificial-intelligence-act-legislative-process';

test('relationship type compatibility label remains readable for record pages', () => {
  assert.equal(relationshipTypeLabel('procedural_step_for'), 'Procedural step for');
});

test('public projection retains every linked endpoint and relationship without mutation', () => {
  const before = JSON.stringify(data);
  const model = createPolicyMapModel(data, '/eu-ai-policy-observatory/');
  assert.equal(model.nodes.length, 100);
  assert.equal(model.edges.length, 95);
  assert.equal(JSON.stringify(data), before);
  assert.ok(model.nodes.every((node) => node.href.startsWith('/eu-ai-policy-observatory/')));
  for (const edge of model.edges) {
    const original = data.relationships.find((relationship) => relationship.id === edge.id);
    assert.equal(edge.source, `${original.source_entity_type}:${original.source_entity_id}`);
    assert.equal(edge.target, `${original.target_entity_type}:${original.target_entity_id}`);
    assert.equal(edge.sourceEntityId, original.source_entity_id);
    assert.equal(edge.targetEntityId, original.target_entity_id);
  }
});

test('principal and expanded family views preserve membership, context and recorded edges', () => {
  const model = createPolicyMapModel(data, '/');
  const principal = selectPolicyMapView(model, family, 'principal');
  const all = selectPolicyMapView(model, family, 'all');
  assert.equal(principal.nodes.length, 9);
  assert.equal(principal.edges.length, 7);
  assert.ok(principal.nodes.every((node) => !node.context && node.level === 'principal'));
  assert.equal(all.memberCount, 40);
  assert.equal(all.nodes.length, 49);
  assert.ok(all.nodes.filter((node) => node.context).every((node) => !node.policyIds.includes(family)));
});

test('projection supports root and subpath routes plus document and policy endpoints', () => {
  const fixture = { generated_at: '2026-01-01', sources: [], events: [], concepts: [], institutions: [], coverage: {}, policies: [{ id: 'policy', short_name: 'Policy', scope_note: 'Scope' }], documents: [{ id: 'document', slug: 'document', short_title: 'Document', document_date: '2025-01-01', document_type: 'proposal', record_level: 'principal', corpus_assessment: null, policies: [{ id: 'policy' }] }], relationships: [{ id: 'edge', source_entity_type: 'policy', source_entity_id: 'policy', target_entity_type: 'document', target_entity_id: 'document', relationship_type: 'contains', basis: 'official', rationale: 'Recorded', evidence_source_id: null }] };
  assert.deepEqual(createPolicyMapModel(fixture, '/').nodes.map((node) => node.href), ['/policies/policy/', '/corpus/document/']);
  assert.deepEqual(createPolicyMapModel(fixture, '/observatory').nodes.map((node) => node.href), ['/observatory/policies/policy/', '/observatory/corpus/document/']);
  assert.throws(() => createPolicyMapModel({ ...fixture, relationships: [{ ...fixture.relationships[0], target_entity_id: 'missing' }] }, '/'), /Unresolved policy map endpoint/);
  assert.throws(() => createPolicyMapModel({ ...fixture, relationships: [{ ...fixture.relationships[0], target_entity_type: 'event' }] }, '/'), /Unsupported policy map endpoint type/);
  assert.deepEqual(createPolicyMapModel({ ...fixture, relationships: [] }, '/').nodes, []);
});

test('policy and document endpoints with the same entity ID remain distinct graph nodes', () => {
  const fixture = {
    generated_at: '2026-01-01', sources: [], events: [], concepts: [], institutions: [], coverage: {},
    policies: [{ id: 'shared', short_name: 'Shared policy', scope_note: 'Scope' }],
    documents: [{ id: 'shared', slug: 'shared-document', short_title: 'Shared document', document_date: '2025-01-01', document_type: 'proposal', record_level: 'principal', corpus_assessment: null, policies: [{ id: 'shared' }] }],
    relationships: [{ id: 'edge', source_entity_type: 'policy', source_entity_id: 'shared', target_entity_type: 'document', target_entity_id: 'shared', relationship_type: 'contains', basis: 'official', rationale: 'Recorded', evidence_source_id: null }],
  };
  const model = createPolicyMapModel(fixture, '/');
  assert.deepEqual(model.nodes.map((node) => node.id), ['policy:shared', 'document:shared']);
  assert.deepEqual(model.nodes.map((node) => node.entityId), ['shared', 'shared']);
  assert.deepEqual(model.edges.map((edge) => [edge.source, edge.target]), [['policy:shared', 'document:shared']]);
});

test('label wrapping retains every word', () => {
  const label = 'Coordinated Plan on Artificial Intelligence';
  const lines = wrapPolicyMapLabel(label);
  assert.ok(lines.length > 1);
  assert.equal(lines.join(' '), label);
});

test('atlas geometry is deterministic, non-overlapping and keeps semantic arrow endpoints', async () => {
  const first = await buildPolicyMapAtlas(data, '/');
  const second = await buildPolicyMapAtlas(data, '/');
  assert.deepEqual(second, first);
  assert.equal(Object.keys(first.views).length, first.model.policies.length * 2);
  assert.equal(Object.keys(first.neighborhoods).length, first.model.nodes.length);
  for (const graph of [...Object.values(first.views), ...Object.values(first.neighborhoods)]) {
    for (let index = 0; index < graph.nodes.length; index += 1) {
      const a = graph.nodes[index];
      for (const b of graph.nodes.slice(index + 1)) assert.ok(a.x + a.width <= b.x || b.x + b.width <= a.x || a.y + a.height <= b.y || b.y + b.height <= a.y, `Overlap: ${a.id}, ${b.id}`);
    }
    for (const edge of graph.edges) {
      const source = graph.nodes.find((node) => node.id === edge.source);
      const target = graph.nodes.find((node) => node.id === edge.target);
      const within = (point, node) => point.x >= node.x - 1 && point.x <= node.x + node.width + 1 && point.y >= node.y - 1 && point.y <= node.y + node.height + 1;
      assert.ok(within(edge.points[0], source), `Wrong source: ${edge.id}`);
      assert.ok(within(edge.points.at(-1), target), `Wrong target: ${edge.id}`);
    }
  }
  for (const [id, graph] of Object.entries(first.neighborhoods)) {
    const expected = first.model.edges.filter((edge) => edge.source === id || edge.target === id);
    assert.deepEqual(graph.edges.map((edge) => edge.id).sort(), expected.map((edge) => edge.id).sort());
  }
});

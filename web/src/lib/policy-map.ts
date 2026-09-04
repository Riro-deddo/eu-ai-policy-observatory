export const semanticPolicyMapStages = [
  'policy',
  'agenda_setting',
  'coordination',
  'consultation',
  'proposal',
  'negotiation',
  'adoption',
  'implementation',
  'unclassified',
];

export const maxLabelCharacters = 27;
export const policyMapNodeWidth = 260;

const nodeColumnGap = 64;
const nodeGap = 24;
const mapLeftInset = 48;
const nodeStartTop = 68;
export const policyMapNodeTypeBaseline = 18;
export const policyMapNodeLabelBaseline = 42;
export const policyMapNodeLabelLineHeight = 18;
const nodeTopPadding = 20;
const nodeBottomPadding = 18;

function readableVocabularyLabel(value: string): string {
  const readable = value.replaceAll('_', ' ');
  return `${readable.charAt(0).toLocaleUpperCase('en-GB')}${readable.slice(1)}`;
}

export const policyMapStageLabel = readableVocabularyLabel;
export const relationshipTypeLabel = readableVocabularyLabel;

export interface PolicyMapLayoutInput {
  label: string;
  stage: string;
}

export interface PolicyMapGeometry {
  labelLines: string[];
  x: number;
  y: number;
  height: number;
}

export interface PolicyMapLayout<T extends PolicyMapLayoutInput> {
  stages: string[];
  nodes: Array<T & PolicyMapGeometry>;
  width: number;
  height: number;
}

export function policyMapStageX(column: number): number {
  return mapLeftInset + policyMapNodeWidth / 2 + column * (policyMapNodeWidth + nodeColumnGap);
}

export function wrapPolicyMapLabel(label: string): string[] {
  return label.trim().split(/\s+/).reduce<string[]>((lines, word) => {
    const current = lines.at(-1);
    if (current === undefined || `${current} ${word}`.length > maxLabelCharacters) {
      lines.push(word);
    } else {
      lines[lines.length - 1] = `${current} ${word}`;
    }
    return lines;
  }, []);
}

export function layoutPolicyMapNodes<T extends PolicyMapLayoutInput>(nodes: T[]): PolicyMapLayout<T> {
  const populatedStages = new Set(nodes.map((node) => node.stage));
  const unexpectedStages = [...populatedStages]
    .filter((stage) => !semanticPolicyMapStages.includes(stage))
    .sort((first, second) => first.localeCompare(second, 'en-GB'));
  const stages = [
    ...semanticPolicyMapStages.filter((stage) => populatedStages.has(stage)),
    ...unexpectedStages,
  ];
  const nodesByStage = [...nodes]
    .sort((first, second) => first.label.localeCompare(second.label, 'en-GB'))
    .reduce((groups, node) => {
      const stageNodes = groups.get(node.stage) ?? [];
      stageNodes.push(node);
      groups.set(node.stage, stageNodes);
      return groups;
    }, new Map<string, T[]>());
  const positionedNodes = [...nodesByStage.entries()].flatMap(([stage, stageNodes]) => {
    const column = stages.indexOf(stage);
    return stageNodes.reduce<{ nodes: Array<T & PolicyMapGeometry>; nextTop: number }>((placement, node) => {
      const labelLines = wrapPolicyMapLabel(node.label);
      const height = nodeTopPadding + nodeBottomPadding + 22 + labelLines.length * policyMapNodeLabelLineHeight;
      placement.nodes.push({
        ...node,
        labelLines,
        x: policyMapStageX(column),
        y: placement.nextTop + height / 2,
        height,
      });
      placement.nextTop += height + nodeGap;
      return placement;
    }, { nodes: [], nextTop: nodeStartTop }).nodes;
  });

  return {
    stages,
    nodes: positionedNodes,
    width: Math.max(580, stages.length * (policyMapNodeWidth + nodeColumnGap) + 48),
    height: Math.max(260, ...positionedNodes.map((node) => node.y + node.height / 2 + 44)),
  };
}

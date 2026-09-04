import assert from 'node:assert/strict';
import test from 'node:test';

import * as policyMap from '../src/lib/policy-map.ts';

const {
  layoutPolicyMapNodes,
  maxLabelCharacters,
  policyMapStageLabel,
  relationshipTypeLabel,
  wrapPolicyMapLabel,
} = policyMap;

test('policy-map vocabulary labels are readable for expanded stages and relationships', () => {
  assert.equal(policyMapStageLabel('agenda_setting'), 'Agenda setting');
  assert.equal(relationshipTypeLabel('version_of'), 'Version of');
  assert.equal(relationshipTypeLabel('annex_to'), 'Annex to');
  assert.equal(relationshipTypeLabel('procedural_step_for'), 'Procedural step for');
});

test('long current policy labels wrap without losing words and grow node height', () => {
  const label = 'Coordinated Plan on Artificial Intelligence';
  const lines = wrapPolicyMapLabel(label);
  const layout = layoutPolicyMapNodes([
    { id: 'short', label: 'AI Act', stage: 'proposal' },
    { id: 'long', label, stage: 'coordination' },
  ]);
  const shortNode = layout.nodes.find((node) => node.id === 'short');
  const longNode = layout.nodes.find((node) => node.id === 'long');

  assert.ok(shortNode);
  assert.ok(longNode);
  assert.ok(lines.length > 1);
  assert.equal(lines.join(' '), label);
  assert.ok(lines.every((line) => line.length <= maxLabelCharacters));
  assert.equal(longNode.labelLines.join(' '), label);
  assert.ok(longNode.height > shortNode.height);
});

test('policy-map layout preserves semantic stage order and full SVG geometry', () => {
  const layout = layoutPolicyMapNodes([
    { id: 'adoption', label: 'Final AI Act', stage: 'adoption' },
    { id: 'proposal', label: 'AI Act proposal', stage: 'proposal' },
    { id: 'unknown', label: 'Future stage', stage: 'zeta' },
  ]);
  const proposal = layout.nodes.find((node) => node.id === 'proposal');
  const adoption = layout.nodes.find((node) => node.id === 'adoption');

  assert.ok(proposal);
  assert.ok(adoption);
  assert.deepEqual(layout.stages, ['proposal', 'adoption', 'zeta']);
  assert.ok(proposal.x < adoption.x);
  assert.equal(layout.width, 1020);
});

test('stage headings reuse the exact x-coordinate allocated to their node column', () => {
  assert.equal(typeof policyMap.policyMapStageX, 'function');
  const layout = layoutPolicyMapNodes([
    { id: 'proposal', label: 'AI Act proposal', stage: 'proposal' },
    { id: 'adoption', label: 'Final AI Act', stage: 'adoption' },
  ]);

  for (const [index, stage] of layout.stages.entries()) {
    assert.equal(
      layout.nodes.find((node) => node.stage === stage)?.x,
      policyMap.policyMapStageX(index),
    );
  }
});

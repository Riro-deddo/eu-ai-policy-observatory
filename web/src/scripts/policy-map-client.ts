import type { PolicyMapAtlas, PolicyMapLayout, PolicyMapNode } from '../lib/policy-map-types';

const root = document.querySelector<HTMLElement>('[data-policy-map-root]');
if (root) void initialise(root);

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function assertLayout(value: unknown, name: string): asserts value is PolicyMapLayout {
  if (!isRecord(value) || !Array.isArray(value.nodes) || !Array.isArray(value.edges)
    || typeof value.width !== 'number' || typeof value.height !== 'number') {
    throw new Error(`Invalid policy map layout: ${name}`);
  }
  for (const node of value.nodes) {
    if (!isRecord(node) || typeof node.id !== 'string' || typeof node.x !== 'number'
      || typeof node.y !== 'number' || typeof node.width !== 'number'
      || typeof node.height !== 'number' || !Array.isArray(node.lines)) {
      throw new Error(`Invalid policy map node geometry: ${name}`);
    }
  }
  for (const edge of value.edges) {
    if (!isRecord(edge) || typeof edge.id !== 'string' || !Array.isArray(edge.points)
      || edge.points.length < 2 || edge.points.some((point) => (
        !isRecord(point) || typeof point.x !== 'number' || typeof point.y !== 'number'
      ))) {
      throw new Error(`Invalid policy map edge geometry: ${name}`);
    }
  }
}

function assertAtlas(value: unknown): asserts value is PolicyMapAtlas {
  if (!isRecord(value) || !isRecord(value.model) || !Array.isArray(value.model.nodes)
    || !Array.isArray(value.model.edges) || !Array.isArray(value.model.policies)
    || !isRecord(value.views) || !isRecord(value.neighborhoods)) {
    throw new Error('Invalid policy map atlas');
  }
  for (const policy of value.model.policies) {
    if (!isRecord(policy) || typeof policy.id !== 'string') throw new Error('Invalid policy map policy');
    for (const mode of ['principal', 'all']) {
      assertLayout(value.views[`${policy.id}:${mode}`], `${policy.id}:${mode}`);
    }
  }
  for (const node of value.model.nodes) {
    if (!isRecord(node) || typeof node.id !== 'string') throw new Error('Invalid policy map node');
    assertLayout(value.neighborhoods[node.id], `neighborhood:${node.id}`);
  }
  if (!value.views['artificial-intelligence-act-legislative-process:principal']) {
    throw new Error('Missing default policy map view');
  }
}

async function initialise(host: HTMLElement): Promise<void> {
  const find = <T extends Element>(selector: string): T => { const node = host.querySelector<T>(selector); if (!node) throw new Error(`Missing policy map element: ${selector}`); return node; };
  const svgNamespace = 'http://www.w3.org/2000/svg';
  const element = (tag: string, text?: string, className?: string): HTMLElement => { const node = document.createElement(tag); if (text !== undefined) node.textContent = text; if (className) node.className = className; return node; };
  const svgElement = (tag: string, attributes: Record<string, string>): SVGElement => { const node = document.createElementNS(svgNamespace, tag); for (const [name, value] of Object.entries(attributes)) node.setAttribute(name, value); return node; };
  const human = (value: string): string => value.replaceAll('_', ' ');
  const familyControl = find<HTMLSelectElement>('[data-policy-map-family]');
  const scene = find<SVGGElement>('[data-policy-map-scene]');
  const viewport = find<HTMLElement>('[data-policy-map-viewport]');
  const workspace = find<HTMLElement>('[data-policy-map-workspace]');
  const details = find<HTMLElement>('[data-policy-map-details]');
  const inspector = find<HTMLElement>('.policy-map__inspector');
  const hint = find<HTMLElement>('[data-policy-map-hint]');
  let atlas: PolicyMapAtlas;
  let graph: PolicyMapLayout;
  let family = 'artificial-intelligence-act-legislative-process';
  let mode: 'principal' | 'all' = 'principal';
  let selected: string | null = null;
  let focusId: string | null = null;
  let camera = { x: 0, y: 0, scale: 1 };
  let drag: { x: number; y: number; camera: typeof camera } | null = null;
  try {
    const response = await fetch(host.dataset.atlasUrl ?? '');
    if (!response.ok) throw new Error(`Policy map atlas returned ${response.status}`);
    const payload: unknown = await response.json();
    assertAtlas(payload);
    atlas = payload;
  } catch (error) {
    find<HTMLElement>('[data-policy-map-failure]').hidden = false;
    find<HTMLElement>('[data-policy-map-counts]').textContent = 'Interactive map unavailable';
    console.warn(error);
    return;
  }
  const nodeById = new Map(atlas.model.nodes.map((node) => [node.id, node]));
  const applyCamera = (): void => { scene.setAttribute('transform', `translate(${camera.x} ${camera.y}) scale(${camera.scale})`); find<HTMLOutputElement>('[data-policy-map-zoom]').textContent = `${Math.round(camera.scale * 100)}%`; };
  const fit = (minimum = 0): void => { const box = viewport.getBoundingClientRect(); const scale = Math.max(minimum, Math.min(1, (box.width - 30) / graph.width, (box.height - 30) / graph.height)); camera = { scale, x: Math.max(12, (box.width - graph.width * scale) / 2), y: Math.max(12, (box.height - graph.height * scale) / 2) }; applyCamera(); };
  const zoom = (factor: number): void => { const box = viewport.getBoundingClientRect(); const scale = Math.max(.08, Math.min(2.5, camera.scale * factor)); const ratio = scale / camera.scale; camera = { scale, x: box.width / 2 - (box.width / 2 - camera.x) * ratio, y: box.height / 2 - (box.height / 2 - camera.y) * ratio }; applyCamera(); };
  const makeButton = (text: string, action: () => void, className?: string): HTMLButtonElement => { const button = element('button', text, className) as HTMLButtonElement; button.type = 'button'; button.addEventListener('click', action); return button; };
  const makeLink = (text: string, url: string): HTMLAnchorElement => { const link = element('a', text) as HTMLAnchorElement; link.href = url; return link; };
  const updateSelection = (): void => {
    inspector.hidden = !selected;
    const selectedNode = selected ? nodeById.get(selected) : undefined;
    inspector.setAttribute('aria-label', selectedNode?.kind === 'policy' ? 'Selected policy' : 'Selected document');
    const inspectorKind = inspector.querySelector<HTMLElement>('.policy-map__inspector-top span');
    if (inspectorKind) inspectorKind.textContent = selectedNode?.kind === 'policy' ? 'POLICY & EVIDENCE' : 'DOCUMENT & EVIDENCE';
    workspace.classList.toggle('has-selection', Boolean(selected));
    const touching = new Set(selected ? atlas.model.edges.filter((edge) => edge.source === selected || edge.target === selected).flatMap((edge) => [edge.source, edge.target]) : []);
    scene.querySelectorAll<SVGElement>('[data-policy-map-node]').forEach((node) => { const active = node.dataset.policyMapNode === selected; node.classList.toggle('selected', active); node.classList.toggle('dim', Boolean(selected) && !active && !touching.has(node.dataset.policyMapNode ?? '')); node.setAttribute('aria-pressed', String(active)); });
    scene.querySelectorAll<SVGElement>('[data-policy-map-edge]').forEach((edge) => { const active = edge.dataset.source === selected || edge.dataset.target === selected; edge.classList.toggle('selected', active); edge.classList.toggle('dim', Boolean(selected) && !active); });
  };
  const showDetails = (): void => {
    details.replaceChildren(); if (!selected) return;
    const node = nodeById.get(selected); if (!node) return;
    const edges = atlas.model.edges.filter((edge) => edge.source === selected || edge.target === selected);
    const meta = node.kind === 'policy' ? 'Policy record' : `${node.date} · ${human(node.level)}`;
    details.append(element('p', meta, 'policy-map__detail-meta'), element('h2', node.title), element('p', `${human(node.kind)} · ${human(node.stage)}`));
    const actions = element('div', undefined, 'policy-map__detail-actions');
    actions.append(makeButton(focusId ? 'Back to group' : 'Focus connections', () => { if (focusId) { focusId = null; changeView(); } else { focusId = node.id; selected = node.id; graph = atlas.neighborhoods[node.id]!; render(); } }), makeLink('Open record', node.href));
    details.append(actions, element('p', `${edges.length} recorded relationships across all policy groups.`));
    const list = element('ul', undefined, 'policy-map__connections');
    for (const edge of edges) { const outgoing = edge.source === node.id; const other = nodeById.get(outgoing ? edge.target : edge.source); if (!other) continue; const item = element('li'); item.append(element('span', outgoing ? `${human(edge.type)} →` : `← ${human(edge.type)}`, 'policy-map__relation-caption'), makeButton(other.title, () => { focusId = other.id; selected = other.id; graph = atlas.neighborhoods[other.id]!; render(); }, 'policy-map__connection-title')); const disclosure = document.createElement('details'); disclosure.append(element('summary', `${edge.basis === 'official' ? 'Official' : 'Analytical'} relationship · Evidence`), element('p', `${nodeById.get(edge.source)?.title} — ${human(edge.type)} → ${nodeById.get(edge.target)?.title}`), element('p', edge.rationale ?? 'No rationale published.')); if (edge.evidence) disclosure.append(makeLink(edge.evidence.publisher, edge.evidence.url)); item.append(disclosure); list.append(item); }
    details.append(list);
  };
  const render = (): void => {
    scene.replaceChildren();
    for (const edge of graph.edges) { const path = svgElement('path', { d: edge.points.map((point, index) => `${index ? 'L' : 'M'}${point.x},${point.y}`).join(' '), class: `policy-map__edge ${edge.basis}`, 'data-policy-map-edge': edge.id, 'data-source': edge.source, 'data-target': edge.target, 'marker-end': 'url(#policy-map-arrow)' }); const title = svgElement('title', {}); title.textContent = `${nodeById.get(edge.source)?.title} — ${human(edge.type)} → ${nodeById.get(edge.target)?.title}`; path.append(title); scene.append(path); }
    for (const node of graph.nodes) {
      const nodeMeta = node.kind === 'policy' ? 'Policy record' : `${node.date} · ${human(node.level)}`;
      const announcement = node.kind === 'policy'
        ? `${node.title}, policy record. Show relationships.`
        : `${node.title}, ${node.date}. Show relationships.`;
      const group = svgElement('g', { transform: `translate(${node.x} ${node.y})`, class: `policy-map__node${node.context ? ' context' : ''}`, 'data-policy-map-node': node.id, role: 'button', tabindex: '0', 'aria-label': announcement, 'aria-pressed': 'false' });
      group.append(svgElement('rect', { width: String(node.width), height: String(node.height), rx: '4' }));
      const meta = svgElement('text', { x: '16', y: '23', class: 'policy-map__node-date' });
      meta.textContent = nodeMeta;
      group.append(meta);
      const title = svgElement('text', { x: '16', y: '47', class: 'policy-map__node-title' });
      node.lines.forEach((line, index) => { const span = svgElement('tspan', { x: '16', dy: index ? '20' : '0' }); span.textContent = line; title.append(span); });
      group.append(title);
      const stage = svgElement('text', { x: '16', y: String(node.height - 13), class: 'policy-map__node-stage' });
      const connected = graph.edges.some((edge) => edge.source === node.id || edge.target === node.id);
      stage.textContent = connected ? `${node.context ? 'Linked context · ' : ''}${human(node.stage)}` : 'Links in expanded view';
      group.append(stage);
      const select = (): void => { selected = node.id; updateSelection(); showDetails(); };
      group.addEventListener('click', select);
      group.addEventListener('keydown', (event) => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); select(); } });
      scene.append(group);
    }
    find<HTMLElement>('[data-policy-map-title]').textContent = focusId ? `Connections: ${nodeById.get(focusId)?.title}` : atlas.model.policies.find((policy) => policy.id === family)?.title ?? '';
    const documentCount = graph.nodes.filter((node) => node.kind === 'document').length;
    const policyCount = graph.nodes.length - documentCount;
    const nodeCount = policyCount === 0
      ? `${documentCount} documents`
      : `${documentCount} documents · ${policyCount} ${policyCount === 1 ? 'policy' : 'policies'}`;
    find<HTMLElement>('[data-policy-map-counts]').textContent = `${nodeCount} · ${graph.edges.length} relationships${graph.contextCount ? ` · ${graph.contextCount} linked context records` : ''}`;
    find<HTMLElement>('[data-policy-map-scope]').textContent = focusId ? 'This focused view includes every direct recorded relationship for the selected document, including other policy groups.' : mode === 'principal' ? `${graph.hidden} supporting records, attachments and versions are not shown. Only recorded links between visible documents are drawn.` : 'This view includes every linked group record and directly linked context. Dashed node borders identify context.';
    host.querySelectorAll<HTMLButtonElement>('[data-policy-map-mode]').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.policyMapMode === mode && !focusId)));
    updateSelection(); showDetails(); fit(.85);
  };
  const changeView = (): void => { graph = atlas.views[`${family}:${mode}`]!; if (selected && !graph.nodes.some((node) => node.id === selected)) selected = null; render(); };
  familyControl.replaceChildren(...atlas.model.policies.map((policy) => { const option = document.createElement('option'); option.value = policy.id; option.textContent = policy.title; return option; })); familyControl.value = family; familyControl.disabled = false;
  familyControl.addEventListener('change', () => { family = familyControl.value; selected = null; focusId = null; changeView(); });
  host.querySelectorAll<HTMLButtonElement>('[data-policy-map-mode]').forEach((button) => button.addEventListener('click', () => { mode = button.dataset.policyMapMode as 'principal' | 'all'; focusId = null; changeView(); }));
  find<HTMLButtonElement>('[data-policy-map-clear]').addEventListener('click', () => { selected = null; focusId = null; changeView(); });
  const search = find<HTMLInputElement>('[data-policy-map-search]'); const results = find<HTMLElement>('[data-policy-map-search-results]');
  search.addEventListener('input', () => { const query = search.value.toLowerCase().trim(); results.replaceChildren(); results.hidden = !query; if (!query) return; const matches = atlas.model.nodes.filter((node) => `${node.title} ${node.date}`.toLowerCase().includes(query)); if (!matches.length) results.append(element('span', 'No matching linked documents. Try another title or year.')); else for (const node of matches.slice(0, 10)) results.append(makeButton(`${node.title} · ${node.date}`, () => { search.value = ''; results.hidden = true; focusId = node.id; selected = node.id; graph = atlas.neighborhoods[node.id]!; render(); })); });
  find<HTMLButtonElement>('[data-policy-map-zoom-in]').addEventListener('click', () => zoom(1.2)); find<HTMLButtonElement>('[data-policy-map-zoom-out]').addEventListener('click', () => zoom(1 / 1.2)); find<HTMLButtonElement>('[data-policy-map-fit]').addEventListener('click', () => fit()); find<HTMLButtonElement>('[data-policy-map-actual]').addEventListener('click', () => zoom(1 / camera.scale));
  find<HTMLButtonElement>('[data-policy-map-fullscreen]').addEventListener('click', async () => { try { if (document.fullscreenElement) await document.exitFullscreen(); else await workspace.requestFullscreen(); } catch { hint.textContent = 'Full screen is unavailable in this browser.'; } });
  viewport.addEventListener('pointerdown', (event) => { if ((event.target as Element).closest('[data-policy-map-node]') || event.button !== 0) return; drag = { x: event.clientX, y: event.clientY, camera: { ...camera } }; viewport.setPointerCapture(event.pointerId); }); viewport.addEventListener('pointermove', (event) => { if (drag) { camera.x = drag.camera.x + event.clientX - drag.x; camera.y = drag.camera.y + event.clientY - drag.y; applyCamera(); } }); for (const name of ['pointerup', 'pointercancel', 'lostpointercapture']) viewport.addEventListener(name, () => { drag = null; });
  viewport.addEventListener('keydown', (event) => { if ((event.target as Element).closest('[data-policy-map-node]')) return; const moves: Record<string, [number, number]> = { ArrowLeft: [60, 0], ArrowRight: [-60, 0], ArrowUp: [0, 60], ArrowDown: [0, -60] }; const move = moves[event.key]; if (move) { event.preventDefault(); camera.x += move[0]; camera.y += move[1]; applyCamera(); } else if (event.key === '+' || event.key === '=') zoom(1.2); else if (event.key === '-') zoom(1 / 1.2); });
  try {
    changeView();
    host.querySelectorAll<HTMLElement>('[data-enhancement]').forEach((node) => { node.hidden = false; });
  } catch (error) {
    find<HTMLElement>('[data-policy-map-failure]').hidden = false;
    find<HTMLElement>('[data-policy-map-counts]').textContent = 'Interactive map unavailable';
    console.warn(error);
  }
}

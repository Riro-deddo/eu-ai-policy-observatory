export type PolicyMapMode = 'principal' | 'all';
export type PolicyMapNodeKind = 'document' | 'policy';
export interface PolicyMapEvidence { url: string; publisher: string }
export interface PolicyMapPolicy { id: string; title: string; description: string }
export interface PolicyMapNode { id: string; kind: PolicyMapNodeKind; title: string; date: string; level: string; stage: string; policyIds: string[]; href: string }
export interface PolicyMapEdge { id: string; source: string; target: string; type: string; basis: 'official' | 'analytical'; rationale: string | null; evidence: PolicyMapEvidence | null }
export interface PolicyMapModel { nodes: PolicyMapNode[]; edges: PolicyMapEdge[]; policies: PolicyMapPolicy[]; generatedAt: string }
export interface PolicyMapViewNode extends PolicyMapNode { context: boolean }
export interface PolicyMapView { family: string; mode: PolicyMapMode; nodes: PolicyMapViewNode[]; edges: PolicyMapEdge[]; memberCount: number; contextCount: number; hidden: number }
export interface PolicyMapPoint { x: number; y: number }
export interface PolicyMapLayoutNode extends PolicyMapViewNode { x: number; y: number; width: number; height: number; lines: string[] }
export interface PolicyMapLayoutEdge extends PolicyMapEdge { points: PolicyMapPoint[] }
export interface PolicyMapLayout extends Omit<PolicyMapView, 'nodes' | 'edges'> { width: number; height: number; nodes: PolicyMapLayoutNode[]; edges: PolicyMapLayoutEdge[] }
export interface PolicyMapAtlas { model: PolicyMapModel; views: Record<string, PolicyMapLayout>; neighborhoods: Record<string, PolicyMapLayout> }

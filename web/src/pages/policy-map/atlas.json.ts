import type { APIRoute } from 'astro';
import { loadPublicData } from '../../lib/data';
import { buildPolicyMapAtlas } from '../../lib/policy-map';

export const prerender = true;

export const GET: APIRoute = async () => {
  const atlas = await buildPolicyMapAtlas(loadPublicData(), import.meta.env.BASE_URL);
  return new Response(JSON.stringify(atlas), { headers: { 'Content-Type': 'application/json; charset=utf-8' } });
};

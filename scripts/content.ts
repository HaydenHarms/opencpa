/**
 * Content tooling.
 *   validate — parse every content/**\/*.yaml file against the schema and report problems.
 *   build    — validate, then bundle reviewed items into apps/api/src/generated/content.json.
 */
import { readdirSync, readFileSync, statSync, mkdirSync, writeFileSync } from 'node:fs';
import { join, relative } from 'node:path';
import { parse } from 'yaml';
import { Item } from '@opencpa/schema';

const root = join(import.meta.dirname, '..');
const contentDir = join(root, 'content');

function walk(dir: string): string[] {
  return readdirSync(dir).flatMap((name) => {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) return walk(p);
    return /\.ya?ml$/.test(name) ? [p] : [];
  });
}

const files = walk(contentDir);
const items: Item[] = [];
const errors: string[] = [];
const seen = new Map<string, string>();

for (const file of files) {
  const rel = relative(root, file);
  let data: unknown;
  try {
    data = parse(readFileSync(file, 'utf8'));
  } catch (e) {
    errors.push(`${rel}: invalid YAML — ${(e as Error).message}`);
    continue;
  }
  const r = Item.safeParse(data);
  if (!r.success) {
    for (const issue of r.error.issues)
      errors.push(`${rel}: ${issue.path.join('.') || '(root)'} — ${issue.message}`);
    continue;
  }
  const item = r.data;
  const expectedName = `${item.id}.yaml`;
  if (!file.endsWith(expectedName)) errors.push(`${rel}: filename must be ${expectedName}`);
  const dir = item.blueprint.section.toLowerCase();
  if (!rel.startsWith(`content/${dir}/`))
    errors.push(`${rel}: ${item.blueprint.section} items belong in content/${dir}/`);
  const dup = seen.get(item.id);
  if (dup) errors.push(`${rel}: duplicate id ${item.id} (also in ${dup})`);
  seen.set(item.id, rel);
  items.push(item);
}

if (errors.length) {
  console.error(
    `✗ ${errors.length} problem(s) in ${files.length} file(s):\n` +
      errors.map((e) => `  - ${e}`).join('\n'),
  );
  process.exit(1);
}

const reviewed = items.filter((i) => i.review.status === 'reviewed');
console.log(
  `✓ ${files.length} file(s) valid — ${reviewed.length} reviewed, ${items.length - reviewed.length} draft/retired`,
);

if (process.argv[2] === 'build') {
  const out = join(root, 'apps/api/src/generated');
  mkdirSync(out, { recursive: true });
  writeFileSync(join(out, 'content.json'), JSON.stringify(reviewed));
  console.log(
    `✓ bundled ${reviewed.length} reviewed item(s) into apps/api/src/generated/content.json`,
  );
}

import os, re

base = r'C:\Users\manen\Downloads\medwave-site\new-site'

with open(os.path.join(base, 'clinical-research', 'medical-monitoring-and-safety-monitoring.html'), 'r', encoding='utf-8') as f:
    template = f.read()

# ── helpers ──────────────────────────────────────────────────────────────────

def make_page(src, title, h1, hero_p, active_slug, other_slug, other_label):
    html = src
    html = html.replace(
        'Medical Monitoring and Safety Monitoring | Medwave Clinical Research',
        f'{title} | Medwave Clinical Research')
    html = html.replace(
        '<h1>Medical Monitoring and Safety Monitoring</h1>',
        f'<h1>{h1}</h1>')
    html = html.replace(
        '<p>Independent medical oversight and patient safety surveillance throughout your clinical trial.</p>',
        f'<p>{hero_p}</p>')
    # main nav + sidebar: replace the single combined <li> with two separate ones
    # pattern matches both the active variant (class="active") and plain variant
    html = re.sub(
        r'<li><a href="medical-monitoring-and-safety-monitoring\.html"(?:[^>]*)>Medical Monitoring and Safety Monitoring</a></li>',
        f'<li><a href="{active_slug}.html" class="active">{title}</a></li>\n                    <li><a href="{other_slug}.html">{other_label}</a></li>',
        html)
    return html

mm_html = make_page(
    template,
    title='Medical Monitoring',
    h1='Medical Monitoring',
    hero_p='Independent medical oversight throughout your clinical trial.',
    active_slug='medical-monitoring',
    other_slug='safety-monitoring',
    other_label='Safety Monitoring')

sm_html = make_page(
    template,
    title='Safety Monitoring',
    h1='Safety Monitoring',
    hero_p='Patient safety surveillance and pharmacovigilance support throughout your clinical trial.',
    active_slug='safety-monitoring',
    other_slug='medical-monitoring',
    other_label='Medical Monitoring')

with open(os.path.join(base, 'clinical-research', 'medical-monitoring.html'), 'w', encoding='utf-8') as f:
    f.write(mm_html)
print('Created medical-monitoring.html')

with open(os.path.join(base, 'clinical-research', 'safety-monitoring.html'), 'w', encoding='utf-8') as f:
    f.write(sm_html)
print('Created safety-monitoring.html')

# ── update all other pages ────────────────────────────────────────────────────

# For pages INSIDE clinical-research/ (relative path, no prefix)
CR_OLD = '<li><a href="medical-monitoring-and-safety-monitoring.html">Medical Monitoring and Safety Monitoring</a></li>'
CR_NEW = '<li><a href="medical-monitoring.html">Medical Monitoring</a></li>\n                    <li><a href="safety-monitoring.html">Safety Monitoring</a></li>'

# For pages OUTSIDE clinical-research/ (prefixed path)
ROOT_OLD = '<li><a href="clinical-research/medical-monitoring-and-safety-monitoring.html">Medical Monitoring and Safety Monitoring</a></li>'
ROOT_NEW = '<li><a href="clinical-research/medical-monitoring.html">Medical Monitoring</a></li>\n                    <li><a href="clinical-research/safety-monitoring.html">Safety Monitoring</a></li>'

skip = {
    'medical-monitoring-and-safety-monitoring.html',
    'medical-monitoring.html',
    'safety-monitoring.html',
}

for root, dirs, files in os.walk(base):
    for fname in files:
        if not fname.endswith('.html'):
            continue
        if fname in skip:
            continue
        path = os.path.join(root, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = content.replace(CR_OLD, CR_NEW).replace(ROOT_OLD, ROOT_NEW)
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated nav in: {os.path.relpath(path, base)}')

print('Done.')

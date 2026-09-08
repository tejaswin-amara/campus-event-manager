// CampusConnect OD Figma Import — Figma Plugin Engine
// Rebuilds OpenDesign capture IR (.od-figma.json) into native Figma frames, text, vector layers, and styles.

figma.showUI(__html__, { width: 420, height: 560, title: 'CampusConnect Design Engine' });

let LOADED_FONTS = new Set();
const fontKey = (family, style) => `${family} ${style}`;

async function tryLoadFont(family, style) {
  const key = fontKey(family, style);
  if (LOADED_FONTS.has(key)) return true;
  try {
    await figma.loadFontAsync({ family, style });
    LOADED_FONTS.add(key);
    return true;
  } catch (err) {
    return false;
  }
}

async function preloadFonts(fonts) {
  LOADED_FONTS = new Set();
  await tryLoadFont('Inter', 'Regular');
  await tryLoadFont('Inter', 'Medium');
  await tryLoadFont('Inter', 'Semi Bold');
  await tryLoadFont('Inter', 'Bold');
  await tryLoadFont('Inter', 'Extra Bold');
  for (const f of fonts || []) {
    const family = f && f.family;
    if (!family) continue;
    const styles = (f.styles && f.styles.length ? f.styles : ['Regular', 'Bold']);
    for (const style of styles) {
      await tryLoadFont(family, style);
    }
  }
}

function resolveFont(family, style) {
  if (LOADED_FONTS.has(fontKey(family, style))) return { family, style };
  if (LOADED_FONTS.has(fontKey('Inter', style))) return { family: 'Inter', style };
  if (LOADED_FONTS.has(fontKey(family, 'Regular'))) return { family, style: 'Regular' };
  return { family: 'Inter', style: 'Regular' };
}

function clamp01(v) {
  return Math.max(0, Math.min(1, Number(v) || 0));
}

function solidPaint(fill) {
  if (!fill || !fill.color) return null;
  const c = fill.color;
  return {
    type: 'SOLID',
    color: { r: clamp01(c.r), g: clamp01(c.g), b: clamp01(c.b) },
    opacity: fill.opacity == null ? 1 : clamp01(fill.opacity)
  };
}

function toPaints(fills) {
  const out = [];
  for (const f of fills || []) {
    const paint = solidPaint(f);
    if (paint) out.push(paint);
  }
  return out;
}

function toEffects(effects) {
  const out = [];
  for (const e of effects || []) {
    if (!e || e.type !== 'DROP_SHADOW') continue;
    const c = e.color || { r: 0, g: 0, b: 0, a: 0.25 };
    out.push({
      type: 'DROP_SHADOW',
      color: { r: clamp01(c.r), g: clamp01(c.g), b: clamp01(c.b), a: c.a == null ? 0.25 : clamp01(c.a) },
      offset: { x: (e.offset && e.offset.x) || 0, y: (e.offset && e.offset.y) || 0 },
      radius: Math.max(0, e.radius || 0),
      spread: Math.max(0, e.spread || 0),
      visible: true,
      blendMode: 'NORMAL'
    });
  }
  return out;
}

function applyBoxProps(node, spec) {
  const fills = toPaints(spec.fills);
  if ('fills' in node && fills.length) node.fills = fills;
  if (spec.strokes && 'strokes' in node) {
    const strokes = toPaints(spec.strokes);
    if (strokes.length) {
      node.strokes = strokes;
      if (spec.strokeWeight && 'strokeWeight' in node) node.strokeWeight = spec.strokeWeight;
    }
  }
  if ('cornerRadius' in node && typeof spec.cornerRadius === 'number') {
    node.cornerRadius = spec.cornerRadius;
  }
  if (spec.rectangleCornerRadii && 'topLeftRadius' in node) {
    const r = spec.rectangleCornerRadii;
    node.topLeftRadius = r.topLeft || 0;
    node.topRightRadius = r.topRight || 0;
    node.bottomRightRadius = r.bottomRight || 0;
    node.bottomLeftRadius = r.bottomLeft || 0;
  }
  const effects = toEffects(spec.effects);
  if (effects.length && 'effects' in node) node.effects = effects;
  if (typeof spec.opacity === 'number' && 'opacity' in node) node.opacity = spec.opacity;
}

async function buildNode(spec, parent, pax, pay) {
  try {
    if (spec.type === 'TEXT') {
      const t = figma.createText();
      const font = resolveFont(spec.fontFamily || 'Inter', spec.fontStyle || 'Regular');
      t.fontName = font;
      t.characters = spec.characters || '';
      if (spec.fontSize) t.fontSize = Math.max(1, spec.fontSize);
      if (spec.lineHeight) t.lineHeight = { value: spec.lineHeight, unit: 'PIXELS' };
      if (spec.letterSpacing) t.letterSpacing = { value: spec.letterSpacing, unit: 'PIXELS' };
      t.textAlignHorizontal = spec.textAlign || 'LEFT';
      const color = spec.color || { r: 1, g: 1, b: 1 };
      t.fills = [{
        type: 'SOLID',
        color: { r: clamp01(color.r), g: clamp01(color.g), b: clamp01(color.b) },
        opacity: spec.opacity == null ? 1 : clamp01(spec.opacity)
      }];
      parent.appendChild(t);
      t.x = (spec.x || 0) - pax;
      t.y = (spec.y || 0) - pay;
      return t;
    }

    const hasChildren = Array.isArray(spec.children) && spec.children.length;
    const node = spec.type === 'RECTANGLE' && !hasChildren ? figma.createRectangle() : figma.createFrame();
    node.name = spec.name || (spec.type === 'RECTANGLE' ? 'Rectangle' : 'Frame');
    
    if (node.type === 'FRAME') {
      node.clipsContent = !!spec.clipsContent;
      if (spec.layoutMode) {
        node.layoutMode = spec.layoutMode;
        if (spec.primaryAxisAlignItems) node.primaryAxisAlignItems = spec.primaryAxisAlignItems;
        if (spec.counterAxisAlignItems) node.counterAxisAlignItems = spec.counterAxisAlignItems;
        if (spec.itemSpacing) node.itemSpacing = spec.itemSpacing;
        if (spec.paddingLeft) node.paddingLeft = spec.paddingLeft;
        if (spec.paddingRight) node.paddingRight = spec.paddingRight;
        if (spec.paddingTop) node.paddingTop = spec.paddingTop;
        if (spec.paddingBottom) node.paddingBottom = spec.paddingBottom;
      }
    }

    node.resize(Math.max(1, spec.width || 1), Math.max(1, spec.height || 1));
    applyBoxProps(node, spec);
    parent.appendChild(node);
    node.x = (spec.x || 0) - pax;
    node.y = (spec.y || 0) - pay;

    if (hasChildren) {
      const nodeAbsX = spec.x || 0;
      const nodeAbsY = spec.y || 0;
      for (const child of spec.children) {
        await buildNode(child, node, nodeAbsX, nodeAbsY);
      }
    }
    return node;
  } catch (e) {
    console.error('Failed to create node', spec, e);
    return null;
  }
}

async function importIr(ir) {
  await preloadFonts(ir.fonts);
  const root = ir.root;
  const container = figma.createFrame();
  container.name = (ir.source && ir.source.title) || root.name || 'CampusConnect Screen';
  container.clipsContent = true;
  container.resize(Math.max(1, root.width || 1440), Math.max(1, root.height || 900));
  applyBoxProps(container, root);
  
  if (!container.fills || !container.fills.length) {
    container.fills = [{ type: 'SOLID', color: { r: 0.035, g: 0.035, b: 0.043 } }]; // #09090B
  }
  
  figma.currentPage.appendChild(container);
  container.x = typeof root.x === 'number' ? root.x : 0;
  container.y = typeof root.y === 'number' ? root.y : 0;

  for (const child of root.children || []) {
    await buildNode(child, container, 0, 0);
  }

  return container;
}

figma.ui.onmessage = async (msg) => {
  if (!msg) return;
  if (msg.type === 'cancel') {
    figma.closePlugin();
    return;
  }
  if (msg.type === 'import') {
    try {
      const ir = msg.ir;
      if (!ir || !ir.root) throw new Error('Invalid capture: missing root.');
      const container = await importIr(ir);
      figma.currentPage.selection = [container];
      figma.viewport.scrollAndZoomIntoView([container]);
      figma.ui.postMessage({ type: 'done', name: container.name });
      figma.notify(`Successfully imported “${container.name}” into Figma!`);
    } catch (err) {
      figma.ui.postMessage({ type: 'error', message: String((err && err.message) || err) });
    }
  }
  if (msg.type === 'import-all') {
    try {
      const screens = msg.screens;
      if (!screens || !Object.keys(screens).length) throw new Error('Missing screens dictionary');
      const containers = [];
      for (const key of Object.keys(screens)) {
        const ir = screens[key];
        if (ir && ir.root) {
          const container = await importIr(ir);
          containers.push(container);
        }
      }
      figma.currentPage.selection = containers;
      figma.viewport.scrollAndZoomIntoView(containers);
      figma.ui.postMessage({ type: 'done', name: `All ${containers.length} screens` });
      figma.notify(`Successfully generated all ${containers.length} screens across Canvas node 0:1!`);
    } catch (err) {
      figma.ui.postMessage({ type: 'error', message: String((err && err.message) || err) });
    }
  }
};

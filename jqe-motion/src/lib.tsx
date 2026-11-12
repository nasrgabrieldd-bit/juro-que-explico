import React from "react";
import { continueRender, delayRender, Easing, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export const C = {
  bg: "#080b09", lime: "#b6f23b", text: "#f4f7f3", gray: "#aab3aa", grid: "#2a352d", card: "#121914", card2: "#19221c",
};

// fontes locais (sem depender de rede)
const fontes: [string, string, number][] = [
  ["Inter", "Inter-Medium.otf", 500], ["Inter", "Inter-SemiBold.otf", 600], ["Inter", "Inter-Bold.otf", 700],
  ["Inter", "Inter-ExtraBold.otf", 800], ["Inter", "Inter-Black.otf", 900], ["InterDisplay", "InterDisplay-Black.otf", 900],
];
let carregadas = false;
export const useFontes = () => {
  const [h] = React.useState(() => (carregadas ? null : delayRender("fontes")));
  React.useEffect(() => {
    if (h === null) return;
    Promise.all(fontes.map(([fam, arq, w]) => {
      const f = new FontFace(fam, `url(${staticFile("fonts/" + arq)})`, { weight: String(w) });
      return f.load().then((ff) => (document as any).fonts.add(ff));
    })).then(() => { carregadas = true; continueRender(h); }).catch(() => continueRender(h));
  }, [h]);
};

export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
export const suave = Easing.bezier(0.16, 1, 0.3, 1);

/** entrada com mola, a partir de `atraso` frames */
export const useEntrada = (atraso = 0, damping = 14) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return spring({ frame: frame - atraso, fps, config: { damping, mass: 0.7 } });
};

/** saída: 0 → 1 nos últimos `n` frames da cena */
export const useSaida = (durFrames: number, n = 8) => {
  const frame = useCurrentFrame();
  return interpolate(frame, [durFrames - n, durFrames], [0, 1], clamp);
};

/** anima o primeiro número de um texto ("R$ 46 mil", "12,8 anos", "0,8%") de 0 até o valor */
export const contar = (texto: string, p: number) => {
  const m = texto.match(/(\d{1,3}(?:\.\d{3})+|\d+)(,\d+)?/);
  if (!m || p >= 1) return texto;
  const inteiro = m[1].replace(/\./g, "");
  const dec = m[2] ? m[2].slice(1) : "";
  const alvo = parseFloat(inteiro + (dec ? "." + dec : ""));
  const v = alvo * Math.max(0, Math.min(1, p));
  const fmt = v.toLocaleString("pt-BR", { minimumFractionDigits: dec.length, maximumFractionDigits: dec.length, useGrouping: m[1].includes(".") });
  return texto.slice(0, m.index) + fmt + texto.slice((m.index || 0) + m[0].length);
};

export const Texto: React.FC<{ children: React.ReactNode; size: number; weight?: number; color?: string; style?: React.CSSProperties; display?: boolean }> =
  ({ children, size, weight = 800, color = C.text, style, display }) => (
    <div style={{ fontFamily: display ? "InterDisplay, Inter" : "Inter", fontSize: size, fontWeight: weight, color, lineHeight: 1.08, letterSpacing: "-0.02em", textAlign: "center", ...style }}>{children}</div>
  );

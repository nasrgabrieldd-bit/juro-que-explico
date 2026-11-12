import React from "react";
import { AbsoluteFill, Audio, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { C, clamp, suave, useFontes } from "./lib";
import { Assinatura, Layout, TIPOS } from "./cenas";

export type Props = { rot: any; tempos: any; marca: any; audio: string; sfx?: boolean };

// Caixa segura. Vertical (TikTok, Reels, Shorts): x 92–930, y 260–1400.
// Horizontal (player do YouTube/feed): fora dos 90 px de cima e 120 px de baixo, margem lateral 110.
const SEG_V = { x: 92, y: 260, w: 838, h: 1140, cenaY: 100, cenaH: 800, legY: 935 };
const SEG_H = { x: 110, y: 100, w: 1700, h: 860, cenaY: 120, cenaH: 610, legY: 760 };
let SEG = SEG_V;

const Fundo: React.FC = () => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const dx = (frame * 0.4) % 90, dy = (frame * 0.25) % 90;
  const gx = 50 + 18 * Math.sin(frame / 140), gy = 70 + 10 * Math.cos(frame / 170);
  return (
    <AbsoluteFill style={{ background: C.bg }}>
      <AbsoluteFill style={{ backgroundImage: `linear-gradient(${C.grid}55 1px, transparent 1px), linear-gradient(90deg, ${C.grid}55 1px, transparent 1px)`,
        backgroundSize: "90px 90px", backgroundPosition: `${dx}px ${dy}px` }} />
      <AbsoluteFill style={{ background: `radial-gradient(circle at ${gx}% ${gy}%, rgba(182,242,59,.16), transparent 45%)` }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,.55))", width, height }} />
    </AbsoluteFill>
  );
};

/** legenda em blocos de até 5 palavras, palavra atual em verde */
const Legenda: React.FC<{ texto: string; durF: number; max?: number }> = ({ texto, durF, max = 5 }) => {
  const frame = useCurrentFrame();
  const words = texto.split(/\s+/).filter(Boolean);
  const pesos = words.map((w) => Math.max(2, w.replace(/[^\wÀ-ú0-9]/g, "").length) + 1);
  const total = pesos.reduce((a, b) => a + b, 0);
  let acc = 0;
  const ini = words.map((_, i) => { const v = (acc / total) * durF; acc += pesos[i]; return v; });
  const blocos: number[][] = []; let cur: number[] = [];
  words.forEach((w, i) => { cur.push(i); if (cur.length >= max || /[.!?,;:]$/.test(w) && cur.length >= 3) { blocos.push(cur); cur = []; } });
  if (cur.length) blocos.push(cur);
  const atual = words.findIndex((_, i) => i === words.length - 1 || ini[i + 1] > frame);
  const bloco = blocos.find((b) => b.includes(Math.max(0, atual))) || blocos[0];
  const ent = interpolate(frame - ini[bloco[0]], [0, 5], [0, 1], clamp);
  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "4px 14px", padding: "16px 26px", borderRadius: 22,
      background: "rgba(0,0,0,.62)", scale: String(0.94 + 0.06 * ent), maxWidth: SEG.w }}>
      {bloco.map((i) => (
        <span key={i} style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 50, lineHeight: 1.15,
          color: i === atual ? C.lime : i < atual ? C.text : "rgba(244,247,243,.55)" }}>{words[i]}</span>
      ))}
    </div>
  );
};

const CenaWrap: React.FC<{ children: React.ReactNode; durF: number; primeira: boolean }> = ({ children, durF, primeira }) => {
  const frame = useCurrentFrame();
  const entra = primeira ? 1 : interpolate(frame, [0, 12], [0, 1], { ...clamp, easing: suave });
  const sai = interpolate(frame, [durF - 7, durF], [0, 1], clamp);
  const zoom = 1 + 0.03 * (frame / Math.max(1, durF));
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", opacity: entra * (1 - sai),
      scale: String((0.94 + 0.06 * entra) * zoom * (1 - 0.04 * sai)), translate: `0px ${(1 - entra) * 40 - sai * 30}px` }}>
      {children}
    </AbsoluteFill>
  );
};

export const Video: React.FC<Props> = ({ rot, tempos, marca, audio, sfx = true }) => {
  useFontes();
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width } = useVideoConfig();
  const horiz = width > 1500;
  SEG = horiz ? SEG_H : SEG_V;
  const cenas: any[] = rot.cenas;
  const tmap: Record<string, any> = Object.fromEntries(tempos.cenas.map((c: any) => [c.id, c]));
  const blocos = cenas.map((c, i) => {
    const t = tmap[c.id];
    const ini = Math.round((i === 0 ? 0 : t.inicio) * fps);
    const prox = cenas[i + 1] ? Math.round(tmap[cenas[i + 1].id].inicio * fps) : durationInFrames;
    return { c, t, ini, durF: Math.max(1, prox - ini) };
  });
  return (
    <AbsoluteFill>
      <Fundo />
      <Audio src={staticFile(audio)} />
      {/* marca no topo, dentro da área segura */}
      <div style={{ position: "absolute", left: SEG.x, top: SEG.y - 10, fontFamily: "Inter", fontWeight: 800, fontSize: 30, letterSpacing: "0.06em", color: C.lime }}>
        {marca.nome_topo}<div style={{ width: 70, height: 5, background: C.lime, marginTop: 8, borderRadius: 3 }} /></div>
      {rot.nota_tela && <div style={{ position: "absolute", left: SEG.x, top: SEG.y + 46, fontFamily: "Inter", fontWeight: 500, fontSize: 22, color: C.gray, maxWidth: SEG.w }}>{rot.nota_tela}</div>}
      {/* cenas */}
      <Layout.Provider value={{ w: horiz ? 1500 : 838, horiz }}>
      <div style={{ position: "absolute", left: SEG.x + (SEG.w - (horiz ? 1500 : 838)) / 2, top: SEG.y + SEG.cenaY, width: horiz ? 1500 : 838, height: SEG.cenaH }}>
        {blocos.map(({ c, ini, durF }, i) => {
          const Comp = c.tipo === "assinatura" ? Assinatura : TIPOS[c.tipo];
          if (!Comp) return null;
          return (
            <Sequence key={c.id} from={ini} durationInFrames={durF} layout="none">
              <Sequence from={i === 0 ? -24 : 0} layout="none">
                <CenaWrap durF={i === 0 ? durF + 24 : durF} primeira={i === 0}>
                  <Comp d={c.dados || {}} dur={durF} linhas={marca.assinatura_linhas} tagline={marca.tagline} />
                </CenaWrap>
              </Sequence>
              {sfx && i > 0 && <Audio src={staticFile("whoosh.wav")} volume={0.35} />}
            </Sequence>
          );
        })}
      </div>
      </Layout.Provider>
      {/* legendas sincronizadas */}
      <div style={{ position: "absolute", left: SEG.x, top: SEG.y + SEG.legY, width: SEG.w, display: "flex", justifyContent: "center" }}>
        {blocos.map(({ c, t }) => c.tipo === "assinatura" ? null : (
          <Sequence key={c.id} from={Math.round(t.inicio * fps)} durationInFrames={Math.round(t.dur * fps) + 6} layout="none">
            <Legenda texto={c.leg} durF={Math.round(t.dur * fps)} max={horiz ? 8 : 5} />
          </Sequence>
        ))}
      </div>
      {/* selo (marca d'água) */}
      <div style={{ position: "absolute", left: horiz ? undefined : SEG.x, right: horiz ? 1920 - SEG.x - SEG.w : undefined, width: horiz ? undefined : SEG.w, top: horiz ? SEG.y - 10 : SEG.y + SEG.h - 34, textAlign: "center", fontFamily: "Inter", fontWeight: 700, fontSize: 34, color: "rgba(244,247,243,.42)" }}>{marca.selo_texto}</div>
      {/* barra de progresso */}
      <div style={{ position: "absolute", left: 0, top: 0, height: 8, width: `${(frame / durationInFrames) * 100}%`, background: C.lime }} />
    </AbsoluteFill>
  );
};

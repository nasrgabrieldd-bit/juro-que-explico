import React from "react";
import { interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { evolvePath } from "@remotion/paths";
import { C, clamp, contar, suave, Texto, useEntrada } from "./lib";

type P = { d: any; dur: number };
// largura útil e orientação vêm do contexto (vertical 838 px; horizontal 1500 px)
export const Layout = React.createContext({ w: 838, horiz: false });

const Linhas: React.FC<{ linhas: string[]; atraso?: number; size?: number; corUltima?: string }> = ({ linhas, atraso = 0, size = 64, corUltima }) => {
  const frame = useCurrentFrame();
  return (
    <div>
      {linhas.map((l, i) => {
        const p = interpolate(frame, [atraso + i * 5, atraso + i * 5 + 14], [0, 1], { ...clamp, easing: suave });
        return <Texto key={i} size={size} weight={800} color={i === linhas.length - 1 && corUltima ? corUltima : C.text}
          style={{ opacity: p, translate: `0px ${(1 - p) * 30}px`, marginTop: i ? 10 : 0 }}>{l}</Texto>;
      })}
    </div>
  );
};

/** palavra por palavra subindo (títulos) */
const Cinetico: React.FC<{ texto: string; size: number; cor?: string; atraso?: number; destaque?: string[] }> = ({ texto, size, cor = C.text, atraso = 0, destaque = [] }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: `0 ${size * 0.28}px` }}>
      {texto.split(" ").map((w, i) => {
        const p = interpolate(frame, [atraso + i * 3, atraso + i * 3 + 12], [0, 1], { ...clamp, easing: suave });
        const hl = destaque.some((x) => w.toLowerCase().includes(x.toLowerCase()));
        return <span key={i} style={{ fontFamily: "InterDisplay, Inter", fontWeight: 900, fontSize: size, lineHeight: 1.08, letterSpacing: "-0.02em",
          color: hl ? C.lime : cor, opacity: p, translate: `0px ${(1 - p) * size * 0.5}px`, display: "inline-block" }}>{w}</span>;
      })}
    </div>
  );
};

export const NumeroGrande: React.FC<P> = ({ d }) => {
  const frame = useCurrentFrame();
  const e = useEntrada(0, 12);
  const pulso = 1 + 0.025 * Math.sin(frame / 9);
  // quadro 0 já mostra o número completo (retenção): a contagem só "respira"
  return (
    <div style={{ textAlign: "center" }}>
      <div style={{ scale: String((0.92 + 0.08 * e) * pulso) }}>
        <Texto size={d.valor.length > 9 ? 150 : 210} display weight={900} color={C.lime}
          style={{ textShadow: "0 0 60px rgba(182,242,59,.35)" }}>{d.valor}</Texto>
      </div>
      <div style={{ marginTop: 36 }}><Linhas linhas={d.linhas || []} size={62} /></div>
    </div>
  );
};

export const Titulo: React.FC<P> = ({ d }) => {
  const frame = useCurrentFrame();
  const sub = interpolate(frame, [18, 32], [0, 1], { ...clamp, easing: suave });
  const linhas: string[] = d.titulo || [];
  return (
    <div style={{ textAlign: "center" }}>
      {linhas.map((l, i) => <div key={i} style={{ marginTop: i ? 6 : 0 }}><Cinetico texto={l} size={92} atraso={i * 8} cor={i === linhas.length - 1 ? C.lime : C.text} /></div>)}
      {d.subtitulo && <div style={{ marginTop: 40, opacity: sub, translate: `0px ${(1 - sub) * 20}px` }}>
        <Texto size={44} weight={600} color={C.gray}>{d.subtitulo}</Texto></div>}
    </div>
  );
};

export const Versus: React.FC<P> = ({ d }) => {
  const frame = useCurrentFrame();
  const { horiz } = React.useContext(Layout);
  const a = useEntrada(0, 13), b = useEntrada(6, 13), x = useEntrada(12, 9);
  const card = (txt: string, rot: string, p: number, lado: number, hl: boolean) => {
    const cont = interpolate(frame, [4, 28], [0, 1], { ...clamp, easing: suave });
    return (
      <div style={{ width: horiz ? 520 : 370, padding: "44px 20px", borderRadius: 32, background: hl ? "rgba(182,242,59,.12)" : C.card,
        border: `3px solid ${hl ? C.lime : C.grid}`, translate: horiz ? `0px ${(1 - p) * lado * 160}px` : `${(1 - p) * lado * 300}px 0px`, opacity: p, boxShadow: hl ? "0 0 50px rgba(182,242,59,.18)" : "none" }}>
        <Texto size={txt.length > 9 ? 62 : 80} display weight={900} color={hl ? C.lime : C.text}>{contar(txt, cont)}</Texto>
        {rot && <Texto size={30} weight={600} color={C.gray} style={{ marginTop: 18, lineHeight: 1.25 }}>{rot}</Texto>}
      </div>
    );
  };
  return (
    <div style={{ display: "flex", flexDirection: horiz ? "row" : "column", alignItems: "center", justifyContent: "center", gap: horiz ? 60 : 26 }}>
      {card(d.a, d.rotulo_a, a, -1, false)}
      <div style={{ scale: String(x), fontFamily: "InterDisplay, Inter", fontWeight: 900, fontSize: 64, color: C.lime }}>{d.centro || "×"}</div>
      {card(d.b, d.rotulo_b, b, 1, true)}
    </div>
  );
};

export const Formula: React.FC<P> = ({ d }) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [0, 12], [0, 1], { ...clamp, easing: suave });
  const linha = d.linha1 || "";
  const chars = Math.round(interpolate(frame, [6, 6 + linha.length * 0.9], [0, linha.length], clamp));
  const r = useEntrada(10 + linha.length * 0.9, 10);
  const nota = interpolate(frame, [26 + linha.length * 0.9, 40 + linha.length * 0.9], [0, 1], clamp);
  const sub = interpolate(frame, [20 + linha.length * 0.9, 38 + linha.length * 0.9], [0, 1], { ...clamp, easing: suave });
  return (
    <div style={{ textAlign: "center" }}>
      <Texto size={40} weight={700} color={C.gray} style={{ opacity: t, textTransform: "uppercase", letterSpacing: "0.08em" }}>{d.titulo}</Texto>
      <div style={{ marginTop: 40, padding: "30px 26px", borderRadius: 26, background: C.card, border: `2px solid ${C.grid}` }}>
        <Texto size={linha.length > 22 ? 50 : 62} weight={800}>{linha.slice(0, chars)}<span style={{ opacity: chars < linha.length ? 1 : 0, color: C.lime }}>|</span></Texto>
      </div>
      <div style={{ marginTop: 36, scale: String(0.6 + 0.4 * r), opacity: r }}>
        <Texto size={d.resultado.length > 12 ? 96 : 130} display weight={900} color={C.lime}>{contar(d.resultado, r)}</Texto>
        <div style={{ height: 10, width: `${sub * 70}%`, margin: "10px auto 0", background: C.lime, borderRadius: 6, opacity: 0.85 }} />
      </div>
      {d.nota && <Texto size={36} weight={600} color={C.gray} style={{ marginTop: 26, opacity: nota }}>{d.nota}</Texto>}
    </div>
  );
};

export const Barras: React.FC<P> = ({ d }) => {
  const frame = useCurrentFrame();
  const { w: W } = React.useContext(Layout);
  const itens: any[] = d.itens || [];
  const max = Math.max(...itens.map((i) => i.valor));
  const h = interpolate(frame, [0, 12], [0, 1], { ...clamp, easing: suave });
  return (
    <div>
      <div style={{ opacity: h }}>{(d.titulo || []).map((l: string, i: number) => <Texto key={i} size={58} weight={800}>{l}</Texto>)}</div>
      <div style={{ marginTop: 46, display: "flex", flexDirection: "column", gap: 26 }}>
        {itens.map((it, i) => {
          const p = interpolate(frame, [8 + i * 7, 32 + i * 7], [0, 1], { ...clamp, easing: suave });
          const larg = (it.valor / max) * (W - (W > 1000 ? 420 : 260)) * p;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 16 }}>
              <div style={{ width: W > 1000 ? 260 : 170, textAlign: "right", fontFamily: "Inter", fontWeight: 700, fontSize: 32, color: it.destaque ? C.text : C.gray }}>{it.rotulo}</div>
              <div style={{ height: 64, width: Math.max(8, larg), background: it.destaque ? C.lime : "#5d6a60", borderRadius: "0 14px 14px 0",
                boxShadow: it.destaque ? "0 0 36px rgba(182,242,59,.35)" : "none" }} />
              <div style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 36, color: it.destaque ? C.lime : C.text, opacity: p, whiteSpace: "nowrap" }}>{contar(it.texto, p)}</div>
            </div>
          );
        })}
      </div>
      {d.nota && <Texto size={32} weight={600} color={C.gray} style={{ marginTop: 40, opacity: interpolate(frame, [30, 44], [0, 1], clamp) }}>{d.nota}</Texto>}
    </div>
  );
};

export const LinhasGrafico: React.FC<P> = ({ d, dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { w: W, horiz } = React.useContext(Layout);
  const GW = W, GH = horiz ? 480 : 620, pl = 96, pb = 64, pt = 30, pr = 150;
  const series: any[] = d.series || [];
  const xs = series.flatMap((s) => s.pontos.map((p: number[]) => p[0]));
  const xmin = Math.min(...xs), xmax = Math.max(...xs);
  const ymin = d.ymin ?? 0, ymax = d.ymax;
  const X = (x: number) => pl + ((x - xmin) / (xmax - xmin)) * (GW - pl - pr);
  const Y = (y: number) => GH - pb - ((y - ymin) / (ymax - ymin)) * (GH - pb - pt);
  const fmt = (v: number) => v >= 1e6 ? `${(v / 1e6).toLocaleString("pt-BR", { maximumFractionDigits: 1 })} mi` : v >= 1000 ? `${Math.round(v / 1000)} mil` : String(Math.round(v));
  const passos = []; for (let v = ymin; v <= ymax + 1e-6; v += d.y_passo) passos.push(v);
  const fim = Math.min(dur - 10, 3.2 * fps);
  const t = interpolate(frame, [6, fim], [0, 1], { ...clamp, easing: suave });
  return (
    <div>
      <Texto size={44} weight={800} style={{ opacity: interpolate(frame, [0, 10], [0, 1], clamp) }}>{d.titulo}</Texto>
      <svg width={GW} height={GH} style={{ marginTop: horiz ? 10 : 20, overflow: "visible" }}>
        <defs><linearGradient id="ar" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor={C.lime} stopOpacity="0.28" /><stop offset="1" stopColor={C.lime} stopOpacity="0" /></linearGradient></defs>
        {passos.map((v, i) => <g key={i} opacity={interpolate(frame, [i * 2, i * 2 + 10], [0, 1], clamp)}>
          <line x1={pl} x2={GW - pr + 20} y1={Y(v)} y2={Y(v)} stroke={C.grid} strokeWidth={2} />
          <text x={pl - 14} y={Y(v) + 9} fill={C.gray} fontSize={26} fontFamily="Inter" fontWeight={600} textAnchor="end">{fmt(v)}</text></g>)}
        {(d.x_ticks || []).map((x: number) => <text key={x} x={X(x)} y={GH - pb + 44} fill={C.gray} fontSize={26} fontFamily="Inter" fontWeight={600} textAnchor="middle">{x}</text>)}
        <text x={(GW - pr + pl) / 2} y={GH + 18} fill={C.gray} fontSize={26} fontFamily="Inter" textAnchor="middle">{d.x_rotulo}</text>
        {series.map((s, si) => {
          const pts: number[][] = s.pontos;
          const path = pts.map((p, i) => `${i ? "L" : "M"}${X(p[0]).toFixed(1)},${Y(p[1]).toFixed(1)}`).join(" ");
          const ev = evolvePath(t, path);
          const n = Math.max(1, Math.floor(t * (pts.length - 1)));
          const head = pts[Math.min(pts.length - 1, n)];
          const area = `${path} L${X(pts[pts.length - 1][0])},${Y(ymin)} L${X(pts[0][0])},${Y(ymin)} Z`;
          const cor = s.destaque ? C.lime : "#8a978d";
          return <g key={si}>
            {s.destaque && <path d={area} fill="url(#ar)" opacity={t >= 1 ? 1 : 0.0 + t * 0.6} clipPath={undefined} />}
            <path d={path} fill="none" stroke={cor} strokeWidth={s.destaque ? 9 : 6} strokeLinecap="round" strokeLinejoin="round"
              strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />
            <circle cx={X(head[0])} cy={Y(head[1])} r={s.destaque ? 13 : 10} fill={cor} />
            <text x={X(head[0]) + 18} y={Y(head[1]) + (s.destaque ? -14 : 30)} fill={cor} fontSize={32} fontFamily="Inter" fontWeight={800}>
              {t >= 1 ? s.rotulo_final : fmt(head[1])}</text>
          </g>;
        })}
      </svg>
      {series.length > 1 && <div style={{ display: "flex", justifyContent: "center", gap: 30, marginTop: horiz ? 34 : 30 }}>
        {series.map((s, i) => <div key={i} style={{ display: "flex", alignItems: "center", gap: 10, fontFamily: "Inter", fontWeight: 700, fontSize: 28, color: C.gray }}>
          <div style={{ width: 34, height: 8, borderRadius: 4, background: s.destaque ? C.lime : "#8a978d" }} />{s.nome}</div>)}
      </div>}
    </div>
  );
};

export const Lista: React.FC<P> = ({ d }) => {
  const frame = useCurrentFrame();
  const itens: string[] = d.itens || [];
  return (
    <div>
      {(d.titulo || []).map((l: string, i: number) => <Cinetico key={i} texto={l} size={76} />)}
      <div style={{ marginTop: 50, display: "flex", flexDirection: "column", gap: 28 }}>
        {itens.map((it, i) => {
          const a = 10 + i * 12;
          const p = interpolate(frame, [a, a + 14], [0, 1], { ...clamp, easing: suave });
          const ck = interpolate(frame, [a + 6, a + 16], [0, 1], clamp);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 24, padding: "24px 28px", borderRadius: 24, background: C.card,
              border: `2px solid ${C.grid}`, opacity: p, translate: `${(1 - p) * -80}px 0px` }}>
              <svg width={56} height={56} viewBox="0 0 56 56"><rect x={2} y={2} width={52} height={52} rx={14} fill="rgba(182,242,59,.14)" stroke={C.lime} strokeWidth={3} />
                <path d="M15 29 L25 39 L42 18" fill="none" stroke={C.lime} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={50} strokeDashoffset={50 * (1 - ck)} /></svg>
              <div style={{ fontFamily: "Inter", fontWeight: 800, fontSize: 44, color: C.text }}>{it}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export const Cta: React.FC<P> = ({ d }) => {
  const frame = useCurrentFrame();
  const b = useEntrada(14, 9);
  return (
    <div style={{ textAlign: "center" }}>
      {(d.linhas || []).map((l: string, i: number) => <Cinetico key={i} texto={l} size={78} atraso={i * 7} cor={i ? C.lime : C.text} />)}
      <div style={{ display: "inline-flex", alignItems: "center", gap: 16, marginTop: 56, padding: "26px 44px", borderRadius: 999, background: C.lime,
        scale: String(b * (1 + 0.03 * Math.sin(frame / 6))) }}>
        <svg width={44} height={44} viewBox="0 0 24 24"><path d="M4 5h16v10H8l-4 4z" fill="#080b09" /></svg>
        <span style={{ fontFamily: "Inter", fontWeight: 900, fontSize: 46, color: "#080b09" }}>{d.botao || "Comenta aqui"}</span>
      </div>
    </div>
  );
};

export const Assinatura: React.FC<P & { linhas: string[]; tagline: string }> = ({ linhas, tagline }) => {
  const frame = useCurrentFrame();
  const a = useEntrada(0, 11), b = useEntrada(6, 11);
  const t = interpolate(frame, [16, 30], [0, 1], clamp);
  return (
    <div style={{ textAlign: "center" }}>
      <div style={{ scale: String(0.8 + 0.2 * a), opacity: a }}><Texto size={150} display weight={900}>{linhas[0]}</Texto></div>
      <div style={{ scale: String(0.8 + 0.2 * b), opacity: b }}><Texto size={170} display weight={900} color={C.lime}>{linhas[1]}</Texto></div>
      <Texto size={44} weight={600} color={C.gray} style={{ marginTop: 40, opacity: t }}>{tagline}</Texto>
    </div>
  );
};

export const TIPOS: Record<string, React.FC<any>> = {
  numero_grande: NumeroGrande, titulo: Titulo, versus: Versus, formula: Formula, barras: Barras, linhas: LinhasGrafico, lista: Lista, cta: Cta,
};

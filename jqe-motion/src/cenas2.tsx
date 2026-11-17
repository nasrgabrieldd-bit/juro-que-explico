import React from "react";
import { interpolate, useCurrentFrame } from "remotion";
import { evolvePath, getLength, getPointAtLength } from "@remotion/paths";
import { C, clamp, suave, Texto, useEntrada } from "./lib";
import { Layout } from "./cenas";

// ---------------------------------------------------------------------------------------------
// Cenas com personagens, setas e trajetória (skill de produção 2.1, 17/11/2026).
// Personagens originais (Léo e Bia), desenhados em SVG com a paleta da marca. Nenhum personagem de terceiros.
// ---------------------------------------------------------------------------------------------

type Pose = "neutro" | "triste" | "feliz" | "aponta" | "sobe";
const PELE = "#e9efe6", ESCURO = "#2a352d", CALCA = "#3a463d";

/** Personagem em SVG (viewBox 200x330). quem: "leo" (camisa verde-limão) ou "bia" (camisa branca, coque). */
export const Pessoa: React.FC<{ quem?: "leo" | "bia"; pose?: Pose; size?: number; frame: number; style?: React.CSSProperties }> =
  ({ quem = "leo", pose = "neutro", size = 300, frame, style }) => {
    const camisa = quem === "leo" ? C.lime : C.text;
    const bob = Math.sin(frame / 8) * (pose === "feliz" ? 5 : 2.5);
    const piscar = frame % 90 > 85 ? 0.15 : 1;
    const wob = Math.sin(frame / 6);
    const braco = (lado: 1 | -1) => {
      const ox = 100 + lado * 38, oy = 122;
      let ex = 100 + lado * 56, ey = 205 + wob * 4;
      if (pose === "feliz") { ex = 100 + lado * 84; ey = 52 + wob * 8; }
      if (pose === "aponta") { if (lado === 1) { ex = 100 + 98; ey = 118 + wob * 3; } }
      if (pose === "sobe") { ex = 100 + lado * 74; ey = lado === 1 ? 72 + wob * 6 : 150 - wob * 6; }
      if (pose === "triste") { ex = 100 + lado * 50; ey = 215; }
      return <line x1={ox} y1={oy} x2={ex} y2={ey} stroke={camisa} strokeWidth={24} strokeLinecap="round" />;
    };
    const boca = pose === "triste" ? "M84 90 Q100 76 116 90" : pose === "feliz" || pose === "sobe" ? "M80 78 Q100 100 120 78" : "M86 84 Q100 92 114 84";
    return (
      <svg width={size} height={size * 1.65} viewBox="0 0 200 330" style={{ overflow: "visible", ...style }}>
        <g transform={`translate(0 ${bob})`}>
          {/* pernas e tênis */}
          <rect x={70} y={218} width={26} height={84} rx={13} fill={CALCA} />
          <rect x={104} y={218} width={26} height={84} rx={13} fill={CALCA} />
          <rect x={60} y={294} width={42} height={18} rx={9} fill={C.lime} />
          <rect x={98} y={294} width={42} height={18} rx={9} fill={C.lime} />
          {/* braços atrás do tronco */}
          {braco(-1)}{braco(1)}
          {/* tronco */}
          <rect x={58} y={106} width={84} height={126} rx={38} fill={camisa} />
          {quem === "leo" && <text x={100} y={178} textAnchor="middle" fontFamily="InterDisplay, Inter" fontWeight={900} fontSize={34} fill="#080b09">J%</text>}
          {/* cabeça */}
          <circle cx={100} cy={58} r={44} fill={PELE} />
          {quem === "leo" ? <path d="M56 52 Q58 8 104 12 Q144 14 144 52 Q120 30 100 32 Q72 32 56 52Z" fill={ESCURO} />
            : <><path d="M56 56 Q54 10 100 10 Q146 10 144 56 Q122 30 100 30 Q78 30 56 56Z" fill={ESCURO} /><circle cx={100} cy={4} r={20} fill={ESCURO} /></>}
          <ellipse cx={84} cy={60} rx={5.5} ry={6 * piscar} fill={ESCURO} />
          <ellipse cx={116} cy={60} rx={5.5} ry={6 * piscar} fill={ESCURO} />
          {pose === "triste" && <><path d="M72 52 L92 43" stroke={ESCURO} strokeWidth={4} strokeLinecap="round" /><path d="M128 52 L108 43" stroke={ESCURO} strokeWidth={4} strokeLinecap="round" />
            <path d="M138 70 Q146 84 138 92 Q130 84 138 70Z" fill="#f4f7f3" opacity={0.9} /></>}
          <path d={boca} fill="none" stroke={ESCURO} strokeWidth={5} strokeLinecap="round" />
        </g>
      </svg>
    );
  };

/** bloco de dinheiro: altura proporcional ao valor */
const Dinheiro: React.FC<{ valor: number; texto: string; max?: number; cor?: string; largura?: number }> = ({ valor, texto, max = 100, cor = C.lime, largura = 190 }) => {
  const h = Math.max(70, 260 * (valor / max));
  return (
    <div style={{ width: largura, height: h, borderRadius: 26, background: cor === C.lime ? "rgba(182,242,59,.16)" : "rgba(170,179,170,.14)", border: `4px solid ${cor}`,
      display: "flex", alignItems: "center", justifyContent: "center", boxShadow: cor === C.lime ? "0 0 40px rgba(182,242,59,.2)" : "none" }}>
      <Texto size={Math.max(30, Math.min(50, Math.floor((largura - 36) / (String(texto).length * 0.58))))} display weight={900} color={cor} style={{ whiteSpace: "nowrap" }}>{texto}</Texto>
    </div>
  );
};

const Balao: React.FC<{ texto: string; p: number; cor?: string; style?: React.CSSProperties }> = ({ texto, p, cor = C.text, style }) => (
  <div style={{ position: "relative", padding: "18px 26px", borderRadius: 26, background: C.card2, border: `3px solid ${C.grid}`, opacity: p, scale: String(0.7 + 0.3 * p),
    transformOrigin: "bottom left", ...style }}>
    <Texto size={42} weight={800} color={cor}>{texto}</Texto>
  </div>
);

/** S2 — Léo com dinheiro que cai pela metade */
export const PersonagemQueda: React.FC<{ d: any; dur: number }> = ({ d }) => {
  const frame = useCurrentFrame();
  const ent = useEntrada(0, 12);
  const queda = interpolate(frame, [48, 70], [0, 1], { ...clamp, easing: suave });
  const valor = d.antes - (d.antes - d.depois) * queda;
  const balao = useEntrada(22, 10);
  const badge = useEntrada(54, 8);
  const triste = queda > 0.5;
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
      <Balao texto={triste ? d.fala_depois : d.fala_antes} p={balao} cor={triste ? C.gray : C.text} />
      <div style={{ display: "flex", alignItems: "flex-end", justifyContent: "center", gap: 46, height: 560 }}>
        <div style={{ translate: `${(1 - ent) * -200}px 0px`, opacity: ent }}><Pessoa quem="leo" pose={triste ? "triste" : "neutro"} size={300} frame={frame} /></div>
        <div style={{ position: "relative", paddingBottom: 16 }}>
          <Dinheiro valor={valor} texto={`R$ ${Math.round(valor)}`} cor={triste ? C.gray : C.lime} />
          <div style={{ position: "absolute", left: "50%", top: -40, translate: "-50% 0", scale: String(badge), opacity: badge }}>
            <div style={{ padding: "8px 22px", borderRadius: 999, background: C.gray, whiteSpace: "nowrap" }}><Texto size={44} weight={900} color="#080b09">{d.badge}</Texto></div>
          </div>
        </div>
      </div>
    </div>
  );
};

/** seta que se desenha */
const Seta: React.FC<{ x1: number; y1: number; x2: number; y2: number; p: number; cor?: string; largura?: number }> = ({ x1, y1, x2, y2, p, cor = C.lime, largura = 10 }) => {
  const path = `M${x1} ${y1} L${x2} ${y2}`;
  const ev = evolvePath(p, path);
  const ang = Math.atan2(y2 - y1, x2 - x1);
  const ponta = (a: number) => `${x2 - Math.cos(ang + a) * 34},${y2 - Math.sin(ang + a) * 34}`;
  return (
    <g>
      <path d={path} stroke={cor} strokeWidth={largura} strokeLinecap="round" fill="none" strokeDasharray={ev.strokeDasharray} strokeDashoffset={ev.strokeDashoffset} />
      <polyline points={`${ponta(0.5)} ${x2},${y2} ${ponta(-0.5)}`} fill="none" stroke={cor} strokeWidth={largura} strokeLinecap="round" strokeLinejoin="round" opacity={p > 0.92 ? 1 : 0} />
    </g>
  );
};

/** S3 — fluxo com setas: 100 → 50 → 75 (a intuição errada) */
export const FluxoSetas: React.FC<{ d: any; dur: number }> = ({ d }) => {
  const frame = useCurrentFrame();
  const itens: any[] = d.caixas;     // [{texto, tom: "neutro"|"cinza"|"erro"|"ok"}]
  const setas: any[] = d.setas;      // [{rotulo, tom}]
  const A = 150, G = 130;            // altura da caixa e vão da seta
  const ini = (i: number) => 6 + i * 26;
  return (
    <div style={{ position: "relative", width: 838, height: A * itens.length + G * setas.length }}>
      {itens.map((c, i) => {
        const p = useEntrada(ini(i), 12);
        const cor = c.tom === "erro" ? C.text : c.tom === "cinza" ? C.gray : C.lime;
        return (
          <div key={i} style={{ position: "absolute", left: 160, top: i * (A + G), width: 518, height: A, borderRadius: 30, opacity: p, scale: String(0.85 + 0.15 * p),
            background: C.card, border: `4px solid ${cor}`, display: "flex", alignItems: "center", justifyContent: "center", gap: 20 }}>
            <Texto size={Math.max(34, Math.min(74, Math.floor(470 / (String(c.texto).length * 0.56))))} display weight={900} color={cor} style={{ whiteSpace: "nowrap" }}>{c.texto}</Texto>
            {c.selo && <div style={{ position: "absolute", right: -40, top: -30, width: 84, height: 84, borderRadius: 42, background: cor, display: "flex", alignItems: "center", justifyContent: "center", scale: String(useEntrada(ini(i) + 14, 8)) }}>
              <Texto size={54} weight={900} color="#080b09">{c.selo}</Texto></div>}
          </div>
        );
      })}
      <svg width={838} height={A * itens.length + G * setas.length} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        {setas.map((s, i) => {
          const p = interpolate(frame, [ini(i) + 14, ini(i) + 34], [0, 1], { ...clamp, easing: suave });
          const y1 = (i + 1) * A + i * G + 10, y2 = (i + 1) * (A + G) - 10;
          const cor = s.tom === "erro" ? C.text : s.tom === "cinza" ? C.gray : C.lime;
          return (<g key={i}><Seta x1={419} y1={y1} x2={419} y2={y2} p={p} cor={cor} />
            <text x={470} y={(y1 + y2) / 2 + 16} fontFamily="InterDisplay, Inter" fontWeight={900} fontSize={Math.max(30, Math.min(56, Math.floor(368 / (String(s.rotulo).length * 0.54))))} fill={cor} opacity={p}>{s.rotulo}</text></g>);
        })}
      </svg>
    </div>
  );
};

/** S4 — trajetória: o Léo desce 50% e precisa escalar 100% para voltar */
export const Trajetoria: React.FC<{ d: any; dur: number }> = ({ d }) => {
  const frame = useCurrentFrame();
  const W = 838, H = 760;
  const P0 = [190, 240], P1 = [420, 560], P2 = [770, 240];
  const queda = `M${P0[0]} ${P0[1]} L${P1[0]} ${P1[1]}`;
  const subida = `M${P1[0]} ${P1[1]} L${P2[0]} ${P2[1]}`;
  const pQ = interpolate(frame, [4, 40], [0, 1], { ...clamp, easing: suave });
  const pS = interpolate(frame, [58, 128], [0, 1], { ...clamp, easing: suave });
  const lq = getLength(queda), ls = getLength(subida);
  const pos = pS > 0 ? getPointAtLength(subida, ls * pS) : getPointAtLength(queda, lq * pQ);
  const sobe = pS > 0 && pS < 1;
  const evQ = evolvePath(pQ, queda), evS = evolvePath(pS, subida);
  const rot = (t: string, x: number, y: number, p: number, cor: string, s = 50) =>
    <text x={x} y={y} fontFamily="InterDisplay, Inter" fontWeight={900} fontSize={s} fill={cor} opacity={p} textAnchor="middle">{t}</text>;
  const fim = interpolate(frame, [128, 142], [0, 1], clamp);
  return (
    <div style={{ position: "relative", width: W, height: H }}>
      <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        <line x1={P0[0]} y1={P0[1]} x2={P2[0] + 40} y2={P0[1]} stroke={C.grid} strokeWidth={4} strokeDasharray="14 12" />
        <line x1={P1[0] - 110} y1={P1[1]} x2={P1[0] + 110} y2={P1[1]} stroke={C.grid} strokeWidth={4} strokeDasharray="14 12" />
        <path d={queda} stroke={C.gray} strokeWidth={14} strokeLinecap="round" fill="none" strokeDasharray={evQ.strokeDasharray} strokeDashoffset={evQ.strokeDashoffset} />
        <path d={subida} stroke={C.lime} strokeWidth={14} strokeLinecap="round" fill="none" strokeDasharray={evS.strokeDasharray} strokeDashoffset={evS.strokeDashoffset} />
        {rot(d.topo, P0[0] - 100, P0[1] + 16, 1, C.text, 46)}
        {rot(d.fundo, P1[0], P1[1] + 70, pQ > 0.95 ? 1 : 0, C.gray, 50)}
        {rot(d.fim, P2[0] - 30, P0[1] - 215, fim, C.lime, 46)}
        {rot(d.rotulo_queda, 150, 440, pQ > 0.6 ? 1 : 0, C.gray, 54)}
        {rot(d.rotulo_subida, 690, 530, pS > 0.35 ? 1 : 0, C.lime, 70)}
        {pS > 0.4 && rot(d.nota_subida, 690, 578, 1, C.text, 32)}
      </svg>
      <div style={{ position: "absolute", left: pos.x - 60, top: pos.y - 196, translate: "0px 0px" }}>
        <Pessoa quem="leo" pose={sobe ? "sobe" : pS >= 1 ? "feliz" : "triste"} size={120} frame={frame} />
      </div>
    </div>
  );
};

/** S6 — tabela com setas: quanto maior a queda, mais íngreme a volta */
export const TabelaSetas: React.FC<{ d: any; dur: number }> = ({ d }) => {
  const frame = useCurrentFrame();
  const linhas: any[] = d.linhas;  // [{queda, sobe, destaque}]
  return (
    <div>
      <Texto size={50} weight={800} color={C.gray} style={{ marginBottom: 30 }}>{d.titulo}</Texto>
      <div style={{ display: "flex", flexDirection: "column", gap: 34 }}>
        {linhas.map((l, i) => {
          const a = 8 + i * 30;
          const p = interpolate(frame, [a, a + 14], [0, 1], { ...clamp, easing: suave });
          const seta = interpolate(frame, [a + 8, a + 26], [0, 1], { ...clamp, easing: suave });
          const hl = !!l.destaque;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", justifyContent: "space-between", opacity: p, translate: `${(1 - p) * -90}px 0px` }}>
              <div style={{ width: 300, padding: "22px 10px", borderRadius: 24, background: C.card, border: `3px solid ${C.grid}`, textAlign: "center" }}>
                <Texto size={32} weight={600} color={C.gray}>caiu</Texto><Texto size={72} display weight={900} color={C.text}>{l.queda}</Texto></div>
              <svg width={150} height={60} viewBox="0 0 150 60"><Seta x1={8} y1={30} x2={140} y2={30} p={seta} cor={hl ? C.lime : C.gray} largura={hl ? 12 : 9} /></svg>
              <div style={{ width: 330, padding: "22px 10px", borderRadius: 24, background: hl ? "rgba(182,242,59,.14)" : C.card, border: `3px solid ${hl ? C.lime : C.grid}`, textAlign: "center",
                boxShadow: hl ? "0 0 40px rgba(182,242,59,.2)" : "none", scale: String(0.9 + 0.1 * seta) }}>
                <Texto size={32} weight={600} color={C.gray}>precisa subir</Texto><Texto size={72} display weight={900} color={C.lime}>{l.sobe}</Texto></div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

/** S7 — dois personagens lado a lado */
export const Duo: React.FC<{ d: any; dur: number }> = ({ d }) => {
  const frame = useCurrentFrame();
  const a = useEntrada(0, 12), b = useEntrada(14, 12);
  const col = (p: number, quem: "leo" | "bia", pose: Pose, dado: any, destaque: boolean) => (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 14, opacity: p, translate: `0px ${(1 - p) * 120}px`, width: 400 }}>
      <Balao texto={dado.fala} p={p} cor={destaque ? C.lime : C.gray} />
      <Pessoa quem={quem} pose={pose} size={250} frame={frame + (quem === "bia" ? 20 : 0)} />
      <Texto size={34} weight={700} color={C.gray}>{dado.rotulo}</Texto>
      <Dinheiro valor={dado.valor} texto={dado.texto} cor={destaque ? C.lime : C.gray} largura={230} max={120} />
    </div>
  );
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-end", width: 838 }}>
      {col(a, "leo", "triste", d.leo, false)}
      {col(b, "bia", "feliz", d.bia, true)}
    </div>
  );
};

/** Gancho com seta: "−50% → +100%" (usado também no fecho do loop; quadro estático depois de assentar) */
export const GanchoSeta: React.FC<{ d: any; dur: number }> = ({ d }) => {
  const frame = useCurrentFrame();
  const e = useEntrada(0, 12);
  const seta = interpolate(frame, [4, 22], [0, 1], { ...clamp, easing: suave });
  const linhas: string[] = d.linhas || [];
  return (
    <div style={{ textAlign: "center", width: 838 }}>
      <div style={{ position: "relative", height: 640 }}>
        <div style={{ position: "absolute", left: 40, top: 0, scale: String(0.9 + 0.1 * e) }}>
          <Texto size={150} display weight={900} color={C.gray} style={{ textAlign: "left" }}>{d.de}</Texto>
        </div>
        <svg width={838} height={640} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
          <Seta x1={200} y1={190} x2={420} y2={292} p={seta} cor={C.lime} largura={14} />
        </svg>
        <div style={{ position: "absolute", right: 20, top: 330, scale: String(0.9 + 0.1 * e) }}>
          <Texto size={d.valor.length > 6 ? 170 : 210} display weight={900} color={C.lime} style={{ textShadow: "0 0 60px rgba(182,242,59,.35)" }}>{d.valor}</Texto>
        </div>
      </div>
      <div>{linhas.map((l, i) => <Texto key={i} size={60} weight={800} style={{ marginTop: i ? 8 : 0 }}>{l}</Texto>)}</div>
    </div>
  );
};

export const TIPOS2: Record<string, React.FC<any>> = {
  personagem_queda: PersonagemQueda, fluxo_setas: FluxoSetas, trajetoria: Trajetoria, tabela_setas: TabelaSetas, duo: Duo, gancho_seta: GanchoSeta,
};
export { Layout };

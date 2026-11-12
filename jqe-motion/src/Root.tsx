import React from "react";
import { Composition } from "remotion";
import { Video, Props } from "./Video";

const vazio: Props = { rot: { cenas: [] }, tempos: { total: 5, cenas: [] }, marca: { nome_topo: "", selo_texto: "", assinatura_linhas: ["", ""], tagline: "" }, audio: "narracao.wav" };

export const Root: React.FC = () => (<>
  <Composition id="Horizontal" component={Video} width={1920} height={1080} fps={30} durationInFrames={150} defaultProps={vazio}
    calculateMetadata={({ props }) => ({ durationInFrames: Math.ceil(((props as Props).tempos.total + 0.6) * 30) })} />
  <Composition id="Vertical" component={Video} width={1080} height={1920} fps={30} durationInFrames={150} defaultProps={vazio}
    calculateMetadata={({ props }) => ({ durationInFrames: Math.ceil(((props as Props).tempos.total + 0.6) * 30) })} />
</>);

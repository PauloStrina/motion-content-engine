import {AbsoluteFill, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

// Punch-in estilo CapCut: en cada corte (empalme de silencios) el encuadre alterna seco entre
// 100% y 107% — disimula el corte como si fuera un cambio de cámara y le da ritmo.
export const VideoPunch: React.FC<{video: string; cortes: number[]; punch: boolean}> = ({
  video,
  cortes,
  punch,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const idx = cortes.filter((c) => t >= c).length - 1;
  const scale = punch && idx >= 0 && idx % 2 === 1 ? 1.07 : 1;
  return (
    <AbsoluteFill style={{transform: `scale(${scale})`, transformOrigin: '50% 38%'}}>
      <OffthreadVideo src={staticFile(video)} />
    </AbsoluteFill>
  );
};

import {useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORES, COLOR_TIPO} from './Reel';

export const Progreso: React.FC<{tipo: string}> = ({tipo}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const color = COLOR_TIPO[tipo] ?? COLORES.naranja;
  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        height: 12,
        width: `${(frame / Math.max(1, durationInFrames - 1)) * 100}%`,
        backgroundColor: color,
      }}
    />
  );
};

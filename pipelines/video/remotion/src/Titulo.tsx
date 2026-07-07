import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORES, COLOR_TIPO} from './Reel';

export const Titulo: React.FC<{texto: string; tipo: string}> = ({texto, tipo}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const caja = COLOR_TIPO[tipo] ?? COLORES.naranja;
  const textoColor = caja === COLORES.aqua ? COLORES.negro : '#FFFFFF';
  const entrada = spring({frame, fps, config: {damping: 200}, durationInFrames: 18});
  const y = interpolate(entrada, [0, 1], [-140, 0]);

  return (
    <div
      style={{
        position: 'absolute',
        top: 140,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        transform: `translateY(${y}px)`,
        opacity: entrada,
      }}
    >
      <div
        style={{
          fontFamily: 'FuturaM',
          textTransform: 'uppercase',
          fontSize: 58,
          lineHeight: 1.1,
          color: textoColor,
          backgroundColor: caja,
          padding: '18px 40px',
          borderRadius: 14,
          maxWidth: 900,
          textAlign: 'center',
          boxShadow: '0 12px 40px rgba(0,0,0,0.35)',
        }}
      >
        {texto}
      </div>
    </div>
  );
};

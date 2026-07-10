import {interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORES, COLOR_TIPO, Dest, FONT} from './Reel';

const DUR = 1.4; // segundos en pantalla

// Palabra martillo: tarjeta grande con sombra laminada monocolor (tratamiento 2 del kit visual)
export const Destacadas: React.FC<{destacadas: Dest[]; tipo: string}> = ({destacadas, tipo}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const activa = destacadas.find((d) => t >= d.desde && t < d.desde + DUR);
  if (!activa) return null;

  const color = COLOR_TIPO[tipo] ?? COLORES.naranja;
  const f = frame - Math.round(activa.desde * fps);
  const pop = spring({frame: f, fps, config: {damping: 14, stiffness: 160}, durationInFrames: 10});
  const salida = interpolate(t, [activa.desde + DUR - 0.25, activa.desde + DUR], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const laminado = [2, 4, 6, 8, 10].map((px) => `${px}px ${px}px 0 ${color}`).join(', ');

  return (
    <div
      style={{
        position: 'absolute',
        top: '30%',
        left: 40,
        right: 40,
        display: 'flex',
        justifyContent: 'center',
        opacity: salida,
        transform: `scale(${0.7 + 0.3 * pop}) rotate(-2deg)`,
      }}
    >
      <div
        style={{
          fontFamily: FONT,
          textTransform: 'uppercase',
          fontSize: 130,
          lineHeight: 1,
          textAlign: 'center',
          color: '#FFFFFF',
          textShadow: `0 14px 50px rgba(0,0,0,0.5), ${laminado}`,
        }}
      >
        {activa.palabra}
      </div>
    </div>
  );
};

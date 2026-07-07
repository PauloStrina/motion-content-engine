import {spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {COLORES, Linea} from './Reel';

const CONTORNO =
  '0 4px 24px rgba(0,0,0,0.6), -3px -3px 0 #1A1A1A, 3px -3px 0 #1A1A1A, -3px 3px 0 #1A1A1A, 3px 3px 0 #1A1A1A';

const PalabraKaraoke: React.FC<{w: string; desde: number; activa: boolean; dicha: boolean}> = ({w, desde, activa, dicha}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  // pop sutil de la palabra activa (nace apenas más chica y salta a su lugar)
  const pop = activa
    ? spring({frame: frame - Math.round(desde * fps), fps, config: {damping: 12, stiffness: 200}, durationInFrames: 8})
    : 1;
  const scale = activa ? 1 + 0.1 * pop : 1;
  return (
    <span
      style={{
        display: 'inline-block',
        margin: '0 12px',
        color: activa || dicha ? COLORES.naranja : '#FFFFFF',
        transform: `scale(${scale})`,
        textShadow: CONTORNO,
      }}
    >
      {w.toUpperCase()}
    </span>
  );
};

export const Captions: React.FC<{lineas: Linea[]}> = ({lineas}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const linea = lineas.find((l, i) => {
    const fin = i + 1 < lineas.length ? Math.min(l.hasta + 0.08, lineas[i + 1].desde) : l.hasta + 0.08;
    return t >= l.desde && t < fin;
  });
  if (!linea) return null;

  const entrada = spring({
    frame: frame - Math.round(linea.desde * fps),
    fps,
    config: {damping: 200},
    durationInFrames: 5,
  });

  return (
    <div
      style={{
        position: 'absolute',
        left: 40,
        right: 40,
        bottom: 520,
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        fontFamily: 'FuturaM',
        fontSize: 84,
        lineHeight: 1.15,
        opacity: entrada,
        transform: `scale(${0.94 + 0.06 * entrada})`,
      }}
    >
      {linea.palabras.map((p, i) => (
        <PalabraKaraoke key={i} w={p.w} desde={p.desde} activa={t >= p.desde && t < p.hasta} dicha={t >= p.hasta} />
      ))}
    </div>
  );
};

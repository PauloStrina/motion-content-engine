import {Composition} from 'remotion';
import {Reel, ReelProps, FPS} from './Reel';

const demo: ReelProps = {
  video: '',
  titulo: 'El KPI del liderazgo',
  tipo: 'conexion',
  modo: 'crop',
  duracion: 6,
  cortes: [0, 1.7],
  destacadas: [{desde: 2.2, palabra: 'Sorprendido'}],
  lineas: [
    {
      desde: 0.3,
      hasta: 1.6,
      palabras: [
        {w: 'Cuántas', desde: 0.3, hasta: 0.7},
        {w: 'veces', desde: 0.7, hasta: 1.1},
        {w: 'me', desde: 1.1, hasta: 1.25},
        {w: 'vi', desde: 1.25, hasta: 1.6},
      ],
    },
    {
      desde: 1.7,
      hasta: 3.2,
      palabras: [
        {w: 'sorprendido', desde: 1.7, hasta: 2.5},
        {w: 'por', desde: 2.5, hasta: 2.7},
        {w: 'alguien', desde: 2.7, hasta: 3.2},
      ],
    },
  ],
};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Reel"
    component={Reel}
    fps={FPS}
    width={1080}
    height={1920}
    durationInFrames={180}
    defaultProps={demo}
    calculateMetadata={({props}) => ({
      durationInFrames: Math.max(1, Math.round(props.duracion * FPS)),
      props,
    })}
  />
);

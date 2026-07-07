import {AbsoluteFill, Img, OffthreadVideo, continueRender, delayRender, staticFile} from 'remotion';
import {Captions} from './Captions';
import {Titulo} from './Titulo';

export const FPS = 30;

// paleta Motion (tokens del design system)
export const COLORES = {
  negro: '#1A1A1A',
  violeta: '#50235A',
  naranja: '#FF5000',
  aqua: '#9DEDE3',
};
export const COLOR_TIPO: Record<string, string> = {
  problema: COLORES.negro,
  metodo: COLORES.violeta,
  resultados: COLORES.naranja,
  conexion: COLORES.aqua,
};

// Carga manual (no @remotion/fonts): si la fuente falla, el render sigue y el motivo queda en el log
// en vez de un timeout mudo de delayRender.
if (typeof document !== 'undefined') {
  const fuente = new FontFace(
    'FuturaM',
    `url('${staticFile('fonts/FuturaStd-CondensedExtraBd.otf')}') format('opentype')`,
  );
  const espera = delayRender('fuente FuturaM');
  fuente
    .load()
    .then((f) => {
      document.fonts.add(f);
      continueRender(espera);
    })
    .catch((err) => {
      console.error('La fuente FuturaM no cargó:', err);
      continueRender(espera);
    });
}

export type Palabra = {w: string; desde: number; hasta: number};
export type Linea = {desde: number; hasta: number; palabras: Palabra[]};
export type ReelProps = {
  video: string; // archivo en public/ (video limpio de cortar.py); vacío = fondo negro (preview)
  titulo: string;
  tipo: string;
  duracion: number;
  lineas: Linea[];
};

export const Reel: React.FC<ReelProps> = ({video, titulo, tipo, lineas}) => (
  <AbsoluteFill style={{backgroundColor: COLORES.negro}}>
    {video ? <OffthreadVideo src={staticFile(video)} /> : null}
    <Titulo texto={titulo} tipo={tipo} />
    <Captions lineas={lineas} />
    <Img
      src={staticFile('logo-blanco.png')}
      style={{position: 'absolute', right: 48, bottom: 64, width: 170, opacity: 0.92}}
    />
  </AbsoluteFill>
);

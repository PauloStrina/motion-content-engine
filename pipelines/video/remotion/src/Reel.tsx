import {AbsoluteFill, Img, staticFile} from 'remotion';
import {Captions} from './Captions';
import {Destacadas} from './Destacadas';
import {Progreso} from './Progreso';
import {Titulo} from './Titulo';
import {VideoPunch} from './VideoPunch';

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

// La fuente se instala a NIVEL SISTEMA (fontconfig en CI, fuentes de usuario en Windows local):
// Chrome la resuelve por nombre sin fetch ni delayRender — la carga web (FontFace/loadFont)
// congelaba pestañas del renderer en Linux sin importar el modo de Chrome.
export const FONT = "'Futura Std', 'FuturaM', Impact, 'Arial Narrow', sans-serif";

export type Palabra = {w: string; desde: number; hasta: number};
export type Linea = {desde: number; hasta: number; palabras: Palabra[]};
export type Dest = {desde: number; palabra: string};
export type ReelProps = {
  video: string; // archivo en public/ (video limpio de cortar.py); vacío = fondo negro (preview)
  titulo: string;
  tipo: string;
  modo?: string;
  duracion: number;
  cortes?: number[]; // arranque de cada corte (línea de tiempo del reel) — alimenta el punch-in
  destacadas?: Dest[]; // palabras martillo elegidas por el Editor de Video
  lineas: Linea[];
};

export const Reel: React.FC<ReelProps> = ({video, titulo, tipo, modo, lineas, cortes, destacadas}) => (
  <AbsoluteFill style={{backgroundColor: COLORES.negro}}>
    {video ? <VideoPunch video={video} cortes={cortes ?? []} punch={modo !== 'split' && modo !== 'marco'} /> : null}
    <Progreso tipo={tipo} />
    <Titulo texto={titulo} tipo={tipo} />
    <Destacadas destacadas={destacadas ?? []} tipo={tipo} />
    <Captions lineas={lineas} silencioEn={destacadas ?? []} />
    <Img
      src={staticFile('logo-blanco.png')}
      style={{position: 'absolute', right: 48, bottom: 64, width: 170, opacity: 0.92}}
    />
  </AbsoluteFill>
);

import {AbsoluteFill, Img, OffthreadVideo, staticFile} from 'remotion';
import {loadFont} from '@remotion/fonts';
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

loadFont({
  family: 'FuturaM',
  url: staticFile('fonts/FuturaStd-CondensedExtraBd.otf'),
});

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

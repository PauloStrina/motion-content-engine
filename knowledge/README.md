# CONOCIMIENTO OPERATIVO DE MOTION

## 1. Propósito

Esta carpeta conserva los bancos y guías que alimentan la creación editorial de Motion. Su función es permitir aprendizaje acumulativo y trazable sin depender de volver a cargar documentos en cada conversación.

No reemplaza la estrategia canónica. La precedencia es:

1. instrucción explícita más reciente de Paulo;
2. `strategy/ESTRATEGIA_MOTION_CANONICA.md`;
3. bancos activos de `knowledge/banks/`;
4. guías operativas de `knowledge/guides/`;
5. `docs/AUDITORIA_EDITORIAL.md`;
6. manifiestos y código de ejecución;
7. archivos históricos.

La conversación produce decisiones y aprendizajes. GitHub es la memoria persistente que los vuelve gobernables para futuras iteraciones. Los documentos adjuntos al proyecto o copias locales no gobiernan cuando contradicen la versión vigente del repositorio.

## 2. Arquitectura

```text
knowledge/
├── README.md
├── MASTER_BASE_CONOCIMIENTO.md
├── banks/
│   ├── BANCO_SITUACIONES_MOTION.md
│   ├── BANCO_ARTEFACTOS_MOTION.md
│   ├── BANCO_CONCEPTOS_MOTION.md
│   ├── BANCO_EVIDENCIAS_MOTION.md
│   └── BANCO_HOOKS_MOTION.md
└── guides/
    └── GUIA_OPERATIVA_HOOKS.md
```

### Banco de Situaciones

Registra escenas, tensiones y problemas observables del Visionario de la Transformación. Una situación puede ser plausible sin constituir evidencia de un caso real.

### Banco de Artefactos

Documenta qué hace Motion para resolver las situaciones: propósito, componentes, participantes, decisiones, resultados y relación con el Programa de Transformación Digital.

### Banco de Conceptos

Conserva conceptos propios, externos adaptados y marcos de interpretación utilizados por Motion. Registra origen, definición, distinciones, conexiones, formulación pública y aplicación visual sin convertir conceptos externos en propiedad intelectual de Motion.

### Banco de Evidencias

Conserva únicamente casos, cifras, citas y resultados con fuente, alcance, autorización y nivel de anonimización explícitos.

### Banco de Hooks

Conserva hooks aprobados y rechazados, el mecanismo utilizado, la situación de origen, el tipo de contenido, el canal y el aprendizaje derivado.

### Guías

Transforman las definiciones estratégicas y los aprendizajes de los bancos en criterios de creación y revisión. No redefinen estrategia.

## 3. Repositorios sincronizados

La arquitectura vive de manera idéntica en:

- `PauloStrina/motion-content-engine` — repositorio operativo primario;
- `ops-motionco/motion-content-engine` — espejo sincronizado.

Una actualización de conocimiento no se considera terminada hasta que:

1. los mismos archivos fueron modificados en ambos repositorios;
2. el contenido relevante es idéntico;
3. existen PRs equivalentes;
4. se validaron los diffs;
5. ambos PRs fueron aprobados y mergeados.

No se realizan cambios independientes en uno de los espejos sin registrar y corregir la divergencia.

## 4. Proceso de actualización desde el chat

Cada interacción puede producir uno o varios cambios. El flujo obligatorio es:

1. **Detectar el aprendizaje.** Identificar si Paulo confirmó un hecho, corrigió una formulación, aprobó un hook, aportó un caso, introdujo un concepto, redefinió un artefacto o tomó una decisión estratégica.
2. **Explicitar la conclusión estratégica.** Después de una corrección relevante, resumir qué principio mejora la calidad del contenido y qué cambia en futuras piezas.
3. **Clasificar la capa.** Estrategia, situación, artefacto, concepto, evidencia, hook o auditoría editorial.
4. **Clasificar el alcance.** Local, recurrente o general.
5. **Aplicar precedencia.** Una decisión estratégica se actualiza primero y únicamente en la estrategia canónica. Los bancos la referencian, no la duplican.
6. **Verificar evidencia y origen.** No convertir una situación o recuerdo en caso público sin confirmar fuente, alcance y autorización. No presentar un concepto externo como propietario.
7. **Actualizar de forma quirúrgica.** Modificar solo las entradas afectadas; conservar IDs y trazabilidad.
8. **Registrar el aprendizaje editorial.** Guardar borrador, versión aprobada, motivo y alcance cuando exista una corrección relevante.
9. **Replicar en ambos repositorios.** Misma rama temática, mismos archivos y contenido equivalente.
10. **Validar.** Revisar links, IDs, referencias cruzadas, contradicciones y ausencia de datos no autorizados.
11. **Abrir PRs equivalentes.** Describir qué cambió, por qué, fuente y archivos afectados.
12. **Mergear después de aprobación.** Ningún cambio de conocimiento se declara vigente antes del merge en ambos repositorios.

## 5. Criterio de aprendizaje

No toda corrección se convierte en regla general.

- **Local:** aplica a una pieza.
- **Recurrente:** patrón a observar en futuras piezas.
- **General:** regla explícitamente aprobada o confirmada por repetición suficiente.

Los pares borrador → versión final tienen prioridad sobre inferencias abstractas de estilo.

## 6. Confidencialidad y veracidad

- No inventar hechos, cifras, resultados, clientes ni citas.
- No publicar nombres o información identificable sin autorización explícita.
- Toda cifra debe conservar fuente, período, alcance y permiso.
- La redacción pública debe usar la formulación autorizada, aunque exista mayor detalle interno.
- Que ambos repositorios sean accesibles no habilita a cargar información confidencial.

## 7. Relación con la producción de contenido

Antes de redactar una pieza se consultan, en este orden:

1. estrategia y tesis;
2. situación elegida;
3. concepto o artefacto que organiza la explicación;
4. evidencia disponible;
5. guía de hooks y banco de hooks;
6. auditoría editorial.

Después de la aprobación humana, el contenido se carga en `manifiestos/mes_<YYYY-MM>.json`. El repositorio valida, compone, renderiza y programa; no redefine el copy aprobado.
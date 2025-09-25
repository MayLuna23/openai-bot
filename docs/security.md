# 🔐 Análisis de Seguridad y Protección de Datos

## 1. Análisis de los Datos Utilizados  
- El proyecto utiliza datos públicos obtenidos de una fuente abierta (NewsAPI) que incluyen:  
  - Títulos de noticias  
  - Resúmenes  
  - Fechas  
  - Fuente o autor  
- No contienen **PII** (información personal identificable) como:  
  - Nombres completos  
  - Correos electrónicos  
  - Números de teléfono  
- Riesgo directo bajo de exponer datos sensibles.  
- Posible presencia de **datos sensibles indirectos**:  
  - Nombres de personas  
  - Ubicaciones específicas  

---

## 2. Riesgos Identificados  

- **Riesgos de privacidad**  
  - Consultas de usuarios podrían revelar:  
    - Intereses  
    - Ubicación  
    - Afiliaciones políticas  
  - Riesgo de creación de perfiles sensibles.  

- **Riesgos técnicos**  
  - Endpoints desprotegidos expuestos a:  
    - Scraping masivo  
    - Inyección SQL
  - Claves API expuestas en el código.  
  - Consultas maliciosas al agente de IA.  

- **Riesgos legales y de cumplimiento**  
  - Redistribución de contenido público podría generar conflictos con:  
    - Derechos de autor  
    - GDPR u otras regulaciones.  

- **Riesgos de desinformación**  
  - El agente de IA podría amplificar información:  
    - No verificada  
    - Sesgada  

---

## 3. Medidas de Mitigación Propuestas
### 🔑 Protección de Endpoints y Acceso  
- Autenticación:  
  - Uso de token o clave secreta en endpoint de actualización.  
  - Recomendación: JWT en producción.  
- Control de acceso:  
  - Exponer solo información necesaria.  
  - Aplicar **rate limiting** por IP o usuario.  

### 📊 Manejo Seguro de Datos  
- Sanitización y validación:  
  - Consultas parametrizadas (SQLAlchemy).  
  - Validación de entradas del usuario.  
- Anonimización y filtrado:  
  - Uso de anonimización o hashing para PII.  
  - Detección automática de PII (nombres, entidades, etc.).  
- Encriptación y retención:  
  - Encriptación de base de datos.  
  - Política de retención (ej. eliminación de artículos antiguos).  

### 🔒 Protección de Credenciales  
- Uso de **variables de entorno** para claves API.  
- Recomendación: usar un **vault de secretos**.  

---

## 4. Conclusión  

El nivel de riesgo identificado para este proyecto es **medio-bajo**, dado que los datos utilizados son principalmente públicos;  
sin embargo, el uso de una API y un agente de IA introduce desafíos adicionales que requieren atención.  

Hasta el momento se han implementado medidas como el uso de un token para la actualización de datos y la sanitización de entradas,  
lo que constituye un buen punto de partida. No obstante, para llevar este proyecto a un entorno de producción seguro, será fundamental  
aplicar medidas adicionales como:

  - **Uso de anonimización o hashing para PII.**
  - **Detección automática de PII** (nombres, entidades, etc.).  
  - **Rate limiting en la API**  
  - **Encriptación de la base de datos**  
  - **Monitoreo del uso de la API** para detectar anomalías  


Más allá de lo técnico, la seguridad debe entenderse también como un compromiso ético con los usuarios: proteger los datos significa  
generar confianza y garantizar un manejo responsable de la información. Construir un sistema seguro implica no solo reaccionar frente  
a amenazas, sino también anticiparlas mediante prevención, buenas prácticas y una visión a largo plazo donde la privacidad y la  
transparencia sean pilares fundamentales.  

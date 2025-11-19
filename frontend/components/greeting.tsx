import { motion } from "framer-motion";
import { Shield } from "lucide-react";

export const Greeting = () => {
  return (
    <div
      className="mx-auto mt-4 flex size-full max-w-3xl flex-col justify-center px-4 md:mt-16 md:px-8"
      key="overview"
    >
      <motion.div
        animate={{ opacity: 1, y: 0 }}
        className="mb-4 flex items-center gap-3"
        exit={{ opacity: 0, y: 10 }}
        initial={{ opacity: 0, y: 10 }}
        transition={{ delay: 0.4 }}
      >
        <Shield className="size-8 text-primary md:size-10" />
      </motion.div>
      <motion.div
        animate={{ opacity: 1, y: 0 }}
        className="font-semibold text-xl md:text-2xl"
        exit={{ opacity: 0, y: 10 }}
        initial={{ opacity: 0, y: 10 }}
        transition={{ delay: 0.5 }}
      >
        Asistente de Ciberseguridad
      </motion.div>
      <motion.div
        animate={{ opacity: 1, y: 0 }}
        className="text-xl text-zinc-500 md:text-2xl"
        exit={{ opacity: 0, y: 10 }}
        initial={{ opacity: 0, y: 10 }}
        transition={{ delay: 0.6 }}
      >
        ¿Qué amenaza necesitas analizar hoy?
      </motion.div>
      <motion.div
        animate={{ opacity: 1, y: 0 }}
        className="mt-4 text-muted-foreground text-sm"
        exit={{ opacity: 0, y: 10 }}
        initial={{ opacity: 0, y: 10 }}
        transition={{ delay: 0.7 }}
      >
        Puedo ayudarte a analizar correos sospechosos, URLs maliciosas, archivos
        desconocidos y comportamientos anómalos.
      </motion.div>
    </div>
  );
};

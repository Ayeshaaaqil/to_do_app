// frontend/src/pages/_app.tsx
import '../styles/globals.css';
import '../styles/components.css';
import type { AppProps } from 'next/app';
import { motion } from 'framer-motion';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="app-container"
    >
      <Component {...pageProps} />
    </motion.div>
  );
}

export default MyApp;
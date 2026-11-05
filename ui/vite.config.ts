import react from "@vitejs/plugin-react";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  base: "/content/",
  build: { outDir: "build", assetsInlineLimit: 0 },
  server: { proxy: { "/api": process.env.LEDS_API ?? "http://localhost:8080" } },
});

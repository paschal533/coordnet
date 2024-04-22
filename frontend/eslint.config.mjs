// @ts-check
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config({
  files: ["packages/**/*.{ts,tsx}"],
  extends: [eslint.configs.recommended, ...tseslint.configs.recommended],
});
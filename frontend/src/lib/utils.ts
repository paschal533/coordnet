import { HocuspocusProvider } from "@hocuspocus/provider";
import { ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import * as Y from "yjs";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/*
 * Get a string representation of an error, whether it is a string, an Error instance, or an object
 * @param error - The error to get a string representation of
 * @returns A string representation of the error
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const getErrorMessage = (error: any): string => {
  if (typeof error === "string") {
    return error;
  }

  // Check if error is an instance of Error
  if (error instanceof Error) {
    return error.message;
  }

  // Handle error objects (like from API responses)
  const errorObj: { statusText?: string; message?: string } = error;
  if (errorObj?.statusText) {
    return errorObj.statusText;
  }
  if (errorObj?.message) {
    return errorObj.message;
  }

  // Attempt to stringify the error if it is an object
  try {
    const errorString = JSON.stringify(error, null, 2);
    // Avoid returning empty or non-informative strings
    if (errorString && errorString !== "{}" && errorString !== '""') {
      return errorString;
    }
  } catch {
    // Fallback in case of JSON.stringify failure
  }

  return `An error occurred: ${String(error)}`;
};

export const title = (title: string = "") => {
  document.title = `${title} - coordination.network`;
};

export class CustomError extends Error {
  code: string;
  name: string;

  constructor({ code, name, message }: { code: string; name: string; message: string }) {
    super(message);
    this.code = code;
    this.name = name;
    Object.setPrototypeOf(this, CustomError.prototype);
  }
}

export const metaKey = (shortcut: string | number) => {
  const platform = navigator.userAgent.toLowerCase();
  if (platform.includes("mac")) {
    return "⌘" + shortcut;
  } else {
    return "Ctrl + " + shortcut;
  }
};

export const rgbToHex = (r: number, g: number, b: number): string => {
  return (
    "#" +
    [r, g, b]
      .map((x) => {
        const hex = x.toString(16);
        return hex.length === 1 ? "0" + hex : hex;
      })
      .join("")
  );
};

export const createConnectedYDoc = async (
  name: string,
  token: string,
): Promise<[Y.Doc, HocuspocusProvider]> => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  return new Promise((resolve, _reject) => {
    const doc = new Y.Doc();
    const provider = new HocuspocusProvider({
      url: import.meta.env.VITE_CRDT_URL,
      name,
      document: doc,
      token,
      preserveConnection: false,
    });

    let isConnected = false;
    let isSynced = false;

    const checkReady = () => {
      if (isConnected && isSynced) {
        resolve([doc, provider]);
      }
    };

    const onStatus = (event: { status: string }) => {
      if (event.status === "connected") {
        isConnected = true;
        checkReady();
      }
    };

    const onSynced = () => {
      if (provider.isSynced) {
        isSynced = true;
        checkReady();
      }
    };

    provider.on("status", onStatus);
    provider.on("synced", onSynced);
  });
};
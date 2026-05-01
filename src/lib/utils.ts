import { twMerge } from 'tailwind-merge';

type ClassValue = string | number | ClassDictionary | ClassArray | undefined | null | boolean;
interface ClassDictionary {
  [id: string]: any;
}
interface ClassArray extends Array<ClassValue> {}

function clsx(...inputs: ClassValue[]) {
  let result = '';

  for (const input of inputs) {
    if (!input) continue;

    const inputType = typeof input;

    if (inputType === 'string' || inputType === 'number') {
      result += (result ? ' ' : '') + input;
    } else if (Array.isArray(input)) {
      const inner = clsx(...input);
      if (inner) {
        result += (result ? ' ' : '') + inner;
      }
    } else if (inputType === 'object') {
      for (const key in input as ClassDictionary) {
        if (Object.prototype.hasOwnProperty.call(input, key) && (input as ClassDictionary)[key]) {
          result += (result ? ' ' : '') + key;
        }
      }
    }
  }

  return result;
}

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(...inputs));
}

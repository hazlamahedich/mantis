import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Utility function to merge Tailwind CSS classes.
 *
 * @param inputs - List of class names or conditional class objects
 * @returns Merged class name string
 */
export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

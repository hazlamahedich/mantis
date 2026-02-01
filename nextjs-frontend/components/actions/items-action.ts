"use server";

import { cookies } from "next/headers";
import { readItem, deleteItem, createItem } from "@/app/clientService";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { itemSchema } from "@/lib/definitions";

export async function fetchItems(page: number = 1, size: number = 10) {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_access_token")?.value;

  if (!token) {
    return { items: [], total: 0, page: 1, size: 10 };
  }

  const { data, error } = await readItem({
    query: {
      page: page,
      size: size,
    },
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (error) {
    console.error("fetchItems error:", error);
    return { items: [], total: 0, page: 1, size: 10 };
  }

  return data;
}

export async function removeItem(id: string) {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_access_token")?.value;

  if (!token) {
    return { message: "No access token found" };
  }

  const { error } = await deleteItem({
    headers: {
      Authorization: `Bearer ${token}`,
    },
    path: {
      item_id: id,
    },
  });

  if (error) {
    return { message: error };
  }
  revalidatePath("/dashboard");
}

export async function addItem(prevState: any, formData: FormData) {
  const cookieStore = await cookies();
  const token = cookieStore.get("auth_access_token")?.value;

  if (!token) {
    return { message: "No access token found" };
  }

  const validatedFields = itemSchema.safeParse({
    name: formData.get("name"),
    description: formData.get("description"),
    quantity: formData.get("quantity"),
  });

  if (!validatedFields.success) {
    return { errors: validatedFields.error.flatten().fieldErrors };
  }

  const { name, description, quantity } = validatedFields.data;

  const { error } = await createItem({
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: {
      name,
      description,
      quantity,
    },
  });

  if (error) {
    return { message: "Failed to create item" };
  }

  revalidatePath("/dashboard");
  redirect(`/dashboard`);
}

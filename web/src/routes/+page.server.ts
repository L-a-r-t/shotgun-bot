import type { Actions } from "./$types"
import { getDB, model } from "$lib/db/mongo"
import { redirect } from "@sveltejs/kit"

export const actions = {
  default: async ({ request, cookies }) => {
    const formData = await request.formData()
    const db = await getDB() // singleton is implied by mongoose, this is to insure a connection exists

    const phone = formData.get("phone")!.toString()

    await model.create({
      lastName: formData.get("lastName"),
      firstName: formData.get("firstName"),
      email: formData.get("email"),
      phone: phone.includes("+") ? phone : `+33${phone.slice(1)}`,
    })

    throw redirect(303, "/success")
  },
} satisfies Actions

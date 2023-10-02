import mongoose from "mongoose"
import { MONGO_URI } from "$env/static/private"

let client: null | typeof mongoose = null
export async function getDB() {
  if (client) return client
  client = await mongoose.connect(MONGO_URI)
  return client
}

const schema = new mongoose.Schema({
  lastName: String,
  firstName: String,
  email: String,
  phone: String,
})

export const model = mongoose.model("BotData", schema)

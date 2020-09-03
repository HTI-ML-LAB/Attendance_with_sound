import mongoose from "mongoose"
import bcrypt from "bcryptjs"

let Schema = mongoose.Schema

let UserSchema = new Schema({
  image : {type : String, default: null},
  name : String,
  year : {type : String, default : null},
  phone : {type : String, default : null},
  features : {type : Array, default: null},
})

UserSchema.statics = {
  createNew(item){
    return this.create(item)
  },
  findAll(){
    return this.find().exec()
  }
}

module.exports = mongoose.model("user", UserSchema)
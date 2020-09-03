import mongoose from "mongoose"


let Schema = mongoose.Schema

let AttendanceSchema = new Schema({
  name : String,
  date : String,
  firsttime :String,
  lasttime : String,
})

AttendanceSchema.statics = {
  createNew(item){
    return this.create(item)
  },
  findAll(){
    return this.find().exec()
  }
}


module.exports = mongoose.model("attendance", AttendanceSchema) 
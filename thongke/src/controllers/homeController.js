import userModel from "./../models/user"
import attendanceModel from "./../models/attendance"

let getHome = async(req, res) => {

  let attendances = await attendanceModel.findAll()
  let users = await userModel.findAll()
  let attendancess= []
  attendances.map((att) => {
    let last_h = +(att.lasttime.split(":")[0])
    let last_m =  +(att.lasttime.split(":")[1])
    let last_s =  +(att.lasttime.split(":")[2])
    let first_h = +(att.firsttime.split(":")[0])
    let first_m =  +(att.firsttime.split(":")[1])
    let first_s =  +(att.firsttime.split(":")[2])
    let total_s = (last_h-first_h) * 3600 + (last_m - first_m) * 60 + last_s-first_s
    let h = parseInt(total_s/3600)
    let m = parseInt((total_s - h*3600)/60)
    let s = (total_s - h*3600 - m*60)
    att = {
      total : h + ":" + m + ":" + s,
      name : att.name,
      date : att.date,
      firsttime : att.firsttime,
      lasttime : att.lasttime
    }
    attendancess.push(att)
  })

  return res.render("master", {attendances : attendancess, users : users})
}

module.exports = {
  getHome : getHome
}
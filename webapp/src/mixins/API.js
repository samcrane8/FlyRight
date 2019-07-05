//API JAVASCRIPT MIXIN

// define a mixin object
import Vue from 'vue';
import axios from 'axios'
import VueAxios from 'vue-axios'
import qs from 'qs';


Vue.use(VueAxios, axios)

export default {
  methods: {
    //USER API CALLS
    async isLoggedIn(token) {
    	var url = process.env.BUSINESS_LOGIC_HOST + '/user/is_logged_in/'
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async login(username, password) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/o/token/'
      var data = { 'grant_type': 'password',
        client_id: process.env.CLIENT_ID,
        client_secret: process.env.CLIENT_SECRET,
        username,
        password
      };
      data = qs.stringify(data)
      return await axios(
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          data,
          url
        }
      );
    },
    async logout(token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/o/revoke_token/'
      var data = { 'grant_type': 'password',
        client_id: process.env.CLIENT_ID,
        client_secret: process.env.CLIENT_SECRET,
        token
      };
      data = qs.stringify(data)
      return await axios(
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          data,
          url
        }
      );
    },
    async register_pilot(email, password, username,
      mobile_phone_number, remote_pilot_certificate_number,
      first_name, last_name) {
      var body = {email, password, username,
        mobile_phone_number,
        remote_pilot_certificate_number,
        first_name, last_name}
      var url = process.env.BUSINESS_LOGIC_HOST + '/pilot/register/'
      return await axios.post(url,body);
    },
    async get_user_info(token, id) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/user/get/?id='+id
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async get_pilot_info(token, id) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/pilot/get/?id='+id
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async get_current_user_info(token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/user/get_current/'
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async update_user_info(user_info, token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/user/update/'
      return await axios.post(url,user_info, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async update_pilot_info(pilot_info, token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/pilot/update/'
      return await axios.post(url,pilot_info, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async forgot_password(email) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/user/forgot_password/?email='+email
      return await axios.get(url);
    },
    async change_password(old_password, new_password, token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/user/change_password/'
      var body = {old_password, new_password}
      return await axios.post(url,body, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    //DRONE API CALLS
    async get_user_drones(token){
      var url = process.env.BUSINESS_LOGIC_HOST + '/drone/get_user_drones/'
      return await axios.get(url, {
          headers: {'Authorization': 'Bearer ' + token}
        });
    },
    async register_drone(faa_registration_number, description, manufacturer, type, color, name, token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/drone/register_drone/'
      var body = {faa_registration_number, description, manufacturer, type,
              color, name}
      return await axios.post(url,body, {
          headers: {'Authorization': 'Bearer ' + token}
        });
    },
    async delete_drone(drone_array, token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/drone/delete_drone/'
      return await axios.post(url,drone_array, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    /**
     * endpoint to edit drone details.
     * @param {Dict} drone required: id, optional: manufacturer, color, type, name.
     * @param {*} token 
     */
    async edit_drone_details(drone, token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/drone/edit_drone_details/'
      return await axios.post(url,drone, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },

    //MISSION API CALLS
    async register_mission(title, area, description, starts_at, ends_at, type, token) {
      var body = {'title': title, 'area': area, 'description': description,
                  'starts_at': starts_at, 'ends_at': ends_at, 'type': type}
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/register/'
      return await axios.post(url,body,{
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async get_mission_drones(mission_id, token) {
      var body = {'mission_id': mission_id}
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/get_drones/'
      return await axios.post(url,body, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async get_mission_info(mission_id, token){
      var body = {'mission_id': mission_id}
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/get_info/'
      return await axios.post(url, body, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async add_drone_to_mission(drone_id, mission_id, operator_id, token) {
      var body = {drone_id, mission_id, operator_id}
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/add_drone/'
      return await axios.post(url,body, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async remove_drone_from_mission(drone_id, mission_id, token) {
      var body = {drone_id, mission_id}
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/remove_drone/'
      return await axios.post(url,body, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async get_missions(token){
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/get/'
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async post_get_missions(filters, token){
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/get/'
      return await axios.post(url, {filters}, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async get_missions_post(start_datetime, end_datetime, token){
      var body = {start_datetime, end_datetime}
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/get/'
      return await axios.post(url,body, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async delete_mission(mission_id, token) {
      var body = {'mission_id': mission_id}
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/delete/'
      return await axios.post(url,body, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async get_current_missions(token){
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/get_current/'
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async get_past_missions(token){
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/get_past/'
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    async get_upcoming_missions(token){
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/get_upcoming/'
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    // Details must be a dictionary with any combination
    // of 'area', 'description', 'title', 'type', 'starts_at', 'ends_at'. If you don't
    // want to change a value, don't put it in the
    // dictionary, just leave it out. Ex.:
    // to change area, and title and type and starts_at:
    // {
    //   'area': <area description>,
    //   'title': 'New Title'
    //   'type': 'Commercial',
    //   'starts_at': <datetime>
    // }
    // to change title and description and ends_at:
    // {
    //   'title': 'New Title',
    //   'description': 'New description.',
    //   'ends_at': <datetime>
    // }
    async edit_mission_details(details, token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/edit/'
      return await axios.post(url,details, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async edit_clearance(mission_id,new_clearance_state, message, token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/flight/edit_clearance/'
      var body = {'mission_id' : mission_id, 'state': new_clearance_state,
                  'message': message}
      return await axios.post(url,body, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async is_government_official(token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/department/is_government_official/'
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer ' + token}
      });
    },
    //DEPARTMENT CALLS
    async flight_histogram(department_id, start_day, end_day, token){
      var body = {department_id, start_day, end_day}
      var url = process.env.BUSINESS_LOGIC_HOST + '/department/flight_histogram/'
      return await axios.post(url,body, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async message_pilots(message, department_name, token){
      var body = {message, department_name}
      var url = process.env.BUSINESS_LOGIC_HOST + '/department/message_jurisdiction/'
      return await axios.post(url,body, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async get_user_departments(token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/department/get_user_departments/'
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async get_department_info(token, department_id){
      var url = process.env.BUSINESS_LOGIC_HOST + `/department/info/?id=${department_id}`
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async get_departments(token) {
      var url = process.env.BUSINESS_LOGIC_HOST + "/department/get/"
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    // NOTIFICATIONS
    async unread_notification_list(token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/notification/unread/'
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async notification_feed(token, count) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/notification/feed/?count=' + count
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async unread_count(token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/inbox/notifications/api/unread_count/'
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async read_all(token) {
      var url = process.env.BUSINESS_LOGIC_HOST + '/notification/read_all/'
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer '+token}
      });
    },
    async read(token, notification_id) {
      var url = `${process.env.BUSINESS_LOGIC_HOST}/notification/read/?id=${notification_id}`
      return await axios.get(url, {
        headers: {'Authorization': 'Bearer '+token}
      });
    }
  }
}

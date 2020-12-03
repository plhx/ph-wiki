$(function() {
    let updateButton = new IndicatorButton('#update-button')

    let View = Vue.createApp({
        delimiters: ['[[', ']]'],
        data: function() {
            return {
                userinfo: {
                    user_id: '',
                    name: '',
                    password: '',
                    retypepassword: ''
                }
            }
        },
        mounted: function() {
            this.getUserInfo()
        },
        methods: {
            getUserInfo: function() {
                $.ajax({
                    cache: false,
                    method: 'GET',
                    url: '/api/profile'
                }).done((response, textStatus, jqXHR) => {
                    this.userinfo = response
                })
            },
            setUserInfo: function() {
                updateButton.state('loading')
                $.ajax({
                    cache: false,
                    method: 'POST',
                    url: '/api/profile',
                    data: {
                        name: this.userinfo.name,
                        password: this.userinfo.password,
                        retypepassword: this.userinfo.retypepassword
                    }
                }).done((response, textStatus, jqXHR) => {
                    this.userinfo.password = ''
                    this.userinfo.retypepassword = ''
                    updateButton.state('done')
                }).fail((jqXHR, textStatus, errorThrown) => {
                    updateButton.state('fail')
                })
            }
        }
    }).mount('#profile')
})

'use strict'

$(function() {
    let AddUserButton = new IndicatorButton('#add-user-submit')
    let UpdateUserButton = new IndicatorButton('#update-user-submit')
    let RemoveUserButton = new IndicatorButton('#remove-user-submit')

    let View = Vue.createApp({
        delimiters: ['[[', ']]'],
        data: function() {
            return {
                users: [],
                roles: {},
                add: {
                    user_id: '',
                    name: '',
                    password: '',
                    role: 0
                },
                update: {
                    user_id: '',
                    name: '',
                    role: 0
                },
                remove: {
                    user_id: '',
                    name: ''
                }
            }
        },
        mounted: function() {
            this.getUsers()
        },
        methods: {
            getUserById: function(userId) {
                for(let i = 0; i < this.users.length; i++) {
                    if(this.users[i].user_id == userId)
                        return this.users[i]
                }
                return null
            },
            getUsers: function() {
                $.ajax({
                    cache: false,
                    method: 'GET',
                    url: '/api/users'
                }).done((response, textStatus, jqXHR) => {
                    for(let key in response)
                        this[key] = response[key]
                })
            },
            addUserButtonClick: function() {
                this.add = {user_id: '', name: '', role: 0}
                $('#add-user-id, #add-user-name, #add-user-role').removeClass('is-valid is-invalid')
                $('#modal-add-user').modal('show')
            },
            validateAddUserId: function() {
                if(this.add.user_id.length == 0 || !/^[\w-]+$/.test(this.add.user_id)) {
                    $('#add-user-id').addClass('is-invalid').removeClass('is-valid')
                    return false
                }
                $('#add-user-id').addClass('is-valid').removeClass('is-invalid')
                return true
            },
            validateAddUserName: function() {
                if(this.add.name.length == 0) {
                    $('#add-user-name').addClass('is-invalid').removeClass('is-valid')
                    return false
                }
                $('#add-user-name').addClass('is-valid').removeClass('is-invalid')
                return true
            },
            validateAddUserPassword: function() {
                if(this.add.password.length < 8) {
                    $('#add-user-password').addClass('is-invalid').removeClass('is-valid')
                    return false
                }
                $('#add-user-password').addClass('is-valid').removeClass('is-invalid')
                return true
            },
            validateAddUserRole: function() {
                if(this.roles[this.add.role] === undefined) {
                    $('#add-user-role').addClass('is-invalid').removeClass('is-valid')
                    return false
                }
                $('#add-user-role').addClass('is-valid').removeClass('is-invalid')
                return true
            },
            addUserButtonClick: function() {
                let isValid = this.validateAddUserId()
                    * this.validateAddUserName()
                    * this.validateAddUserPassword()
                    * this.validateAddUserRole()
                if(!isValid)
                    return
                AddUserButton.state('loading')
                $.ajax({
                    cache: false,
                    method: 'PUT',
                    url: '/api/user',
                    data: {
                        user_id: this.add.user_id,
                        name: this.add.name,
                        password: this.add.password,
                        role: this.add.role
                    }
                }).done((response, textStatus, jqXHR) => {
                    for(let key in response)
                        this[key] = response[key]
                    $('#modal-add-user').modal('hide')
                    AddUserButton.state('done')
                }).fail((jqXHR, textStatus, errorThrown) => {
                    AddUserButton.state('fail')
                })
            },
            updateUserButtonClick: function(e) {
                let userId = $(e.currentTarget).attr('data-id')
                this.update = this.getUserById(userId)
                $('#modal-update-user').modal('show')
            },
            validateUpdateUserName: function() {
                if(this.update.name.length == 0) {
                    $('#update-user-name').addClass('is-invalid').removeClass('is-valid')
                    return false
                }
                $('#update-user-name').addClass('is-valid').removeClass('is-invalid')
                return true
            },
            validateUpdateUserRole: function() {
                if(this.roles[this.update.role] === undefined) {
                    $('#update-user-role').addClass('is-invalid').removeClass('is-valid')
                    return false
                }
                $('#update-user-role').addClass('is-valid').removeClass('is-invalid')
                return true
            },
            updateUserButtonClick: function() {
                let isValid = this.validateUpdateUserName() * this.validateUpdateUserRole()
                if(!isValid)
                    return
                UpdateUserButton.state('loading')
                $.ajax({
                    cache: false,
                    method: 'POST',
                    url: '/api/user/' + this.update.user_id,
                    data: {
                        name: this.update.name,
                        role: this.update.role
                    }
                }).done((response, textStatus, jqXHR) => {
                    for(let key in response)
                        this[key] = response[key]
                    $('#modal-update-user').modal('hide')
                    UpdateUserButton.state('done')
                }).fail((jqXHR, textStatus, errorThrown) => {
                    UpdateUserButton.state('fail')
                })
            },
            removeUserButtonClick: function(e) {
                let userId = $(e.currentTarget).attr('data-id')
                this.remove = this.getUserById(userId)
                $('#modal-remove-user').modal('show')
            },
            removeUserButtonClick: function() {
                RemoveUserButton.state('loading')
                $.ajax({
                    cache: false,
                    method: 'DELETE',
                    url: '/api/user/' + this.remove.user_id
                }).done((response, textStatus, jqXHR) => {
                    for(let key in response)
                        this[key] = response[key]
                    $('#modal-remove-user').modal('hide')
                    RemoveUserButton.state('done')
                }).fail((jqXHR, textStatus, errorThrown) => {
                    RemoveUserButton.state('fail')
                })
            }
        }
    }).mount('#manage')
})
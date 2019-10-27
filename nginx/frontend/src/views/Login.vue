<template>
    <div class="card">
        <form @submit.prevent="login">
            <label for="username" hidden>username</label>
            <input type="text" id="username" v-model="username" autocomplete="username" placeholder="username">
            <br>
            <label for="password" hidden>password</label>
            <input type="password" id="password" v-model="password" autocomplete="current-password" placeholder="password">
            <br><br>
            <input type="submit" value="Login">
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: ''
        }
    },
    mounted() {
        if (localStorage.getItem('access_token')) {
        this.$store.dispatch('auth/signIn', '')
        }  
    },
    methods: {
        async login() {
            let formData = new FormData()
            formData.append('username', this.username)
            formData.append('password', this.password)
            await this.$store.dispatch('auth/signIn', formData)
        }
    }
}
</script>

<template>                   
	<v-layout class="background">
		<v-flex xs10 sm8 offset-sm2>
			<v-card id="firstCard">
				<template>
					<v-parallax src="/static/firstPic.jpg" width="1000"></v-parallax>
				</template>
			</v-card>
			<v-card id="secondCard">
				<template>
					<v-parallax src="/static/secondPic.jpg"></v-parallax>
				</template>
			</v-card>
		</v-flex>
	</v-layout>
</template>

<script>
</script>

<!-- styling for the component -->
<style>
#firstPic {
	margin-top: 90px;
}
#secondPic {
	margin-top: 10px;
}
</style>


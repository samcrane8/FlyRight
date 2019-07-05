<template>
	<v-card>
		<v-card-title>
			<v-layout column>
				<v-flex>
					<span style="font-size:30px;"> Licenses </span>
				</v-flex>
				<v-layout column>
					<v-layout row
						v-for="doc in profile_info.documents"
						:key = "profile_info.type"
						>
						<v-card style="margin-top: 20px; margin-left: auto; margin-right: auto; width: 400px;">
							<v-toolbar>
							    <v-toolbar-title>{{doc.type}}</v-toolbar-title>
							    <v-spacer></v-spacer>
							    <v-toolbar-items class="hidden-sm-and-down">
							    	<v-btn flat @click='viewFile(doc)'>
										<span> EDIT </span>
									</v-btn>
							      	<v-btn flat @click="doc.show=!doc.show" v-if="!doc.show">
						                <v-icon>arrow_drop_down</v-icon>
						            </v-btn>
						            <v-btn flat @click="doc.show=!doc.show" v-if="doc.show">
						                <v-icon>arrow_drop_up</v-icon>
						            </v-btn>
							    </v-toolbar-items>
							 </v-toolbar>
							<div style="margin-top: 20px; margin-left: auto; margin-right: auto;" v-if="doc.show">
								<pdf :src="doc.location" 
				              		v-if="doc.location!=null"
							      	:page=1
							      	:ref=doc.type
							     	@num-pages="numPages = $event"
							     	style="width:400px; margin-left: auto; margin-right: auto;">
							    </pdf>
							    <div class="box_input" v-if="doc.location==null">
				            		<div class="box_inside">
								  		<v-icon x-large style="margin-top:15%;">error</v-icon>
								  		<br>
								    	<label><strong>No file uploaded</strong></label>
									</div>
				            	</div>
							</div>
							<v-flex xs12 class="text-xs-center text-sm-center text-md-center text-lg-center">
								<input
									type="file"
									style="display: none"
									id="myBtn"
									@change="onFilePicked"
									accept=".pdf"
								>
								<v-dialog v-model="editFile" max-width="500px">
								    <v-card>
								        <v-card-title primary-title>
									        <div>
									        	<h3 class="headline mb-0">{{currFile.type}} Upload</h3>
									          	<div>
									            	<div v-if="pdfUrl==null" class="box_input" @mouseover="mouseOver" @mouseout="mouseOut">
									            		<div class="box_inside">
													  		<v-icon x-large style="margin-top:15%;">file_upload</v-icon>
													  		<br>
													    	<input
																type="file"
																style="display: none"
																id="myBtn"
																@change="onFilePicked"
																accept=".pdf"
															>
													    	<label @click='pickFile'><strong>No file selected</strong></label>
														</div>
									            	</div>
									            	<div>
										            	<pdf :src="pdfUrl" 
										              		v-if="pdfUrl!=null"
													      	:page=1
													     	@num-pages="numPages = $event"
													     	style="width:400px">
													    </pdf>
										            </div>
									            	<h4 style="text-align: center; color: red;" v-if="typeError"> Incorrect File Type. Make sure to upload a PDF </h4>
									          	</div>
									        </div>
								        </v-card-title>
								        <v-card-actions>
								          <v-btn color="primary" flat @click='pickFile'>Upload</v-btn>
								          <v-btn color="primary" flat @click.stop="editFile=false" @click="saveFile()">Save</v-btn>
								          <v-btn color="primary" flat @click.stop="editFile=false" @click="clearFile()">Cancel</v-btn>
								        </v-card-actions>
								    </v-card>
								</v-dialog>
							</v-flex>
						</v-card>
					</v-layout>
				</v-layout>
			</v-layout>
		</v-card-title>
	</v-card>
</template>

<style>
	.box_input {
		width: 400px;
		height: 200px;
		outline: 2px dashed darkgray;
		margin-top: 2%;
		margin-left: auto;
		margin-right: auto;
	}
	.box_inside {
		text-align: center;
	}
</style>

<script>
import API from '../../mixins/API.js'
import Vue from 'vue';
import pdf from 'vue-pdf'
Vue.component('pdf', pdf)
export default {
	mixins: [API],
	props: ['user_info'],
	data() {
		return {
			size:'150px',
			items: [
				{'title': 'Profile'},
				{'title': 'Licenses'},
				{'title': 'Delete'}
			],
			profile_info: {
				image: 'https://avatars0.githubusercontent.com/u/8029035?s=400&v=4',
				documents: [
					{ type: 'Part 107', location: 'https://cdn.mozilla.net/pdfjs/tracemonkey.pdf', show: false},
					{ type: 'Part 333', location: null, show: false}
				]
			},
			pdfUrl: null,
			pdfName: '',
    		pdfFile: '',
    		currFile: {type:null},
    		editFile: false,
    		typeError: false
		}
	},
	methods: {
		pickFile () {
        	document.getElementById("myBtn").click();
        },
        saveFile() {
        	if (this.pdfUrl != null) {
        		var e = this.profile_info.documents[this.profile_info.documents.indexOf(this.currFile)];
	        	e.show=false;
	        	e.location = this.pdfUrl;
	        	this.clearFile();
	        	this.$emit('snackbar',6000, 'File Successfully Saved');
	        }
        },
        clearFile() {
      		this.pdfName = '';
      		this.pdfFile = '';
      		this.pdfUrl = null;
      		this.typeError = false;
      	},
        viewFile(e) {
        	this.currFile = e;
        	this.editFile=true;
        },
      	onFilePicked (e) {
        	const files = e.target.files;
        	if(files[0] !== undefined) {
          		this.pdfName = files[0].name;
          		if(this.pdfName.slice((this.pdfName.lastIndexOf(".") - 1 >>> 0) + 2)!="pdf") {
          			this.typeError = true;
          			return;
          		}
          		if(this.pdfName.lastIndexOf('.') <= 0) {
            		return;
          		}
          		const fr = new FileReader ();
          		fr.readAsDataURL(files[0]);
          		fr.addEventListener('load', () => {
            		this.pdfUrl = fr.result;
            		this.pdfFile = files[0];
          		})
          		this.typeError = false;
        	} else {
        		this.clearFile();
        	}
      	},
      	mouseOver() {
      		document.body.style.cursor= 'pointer';
      	},
      	mouseOut() {
      		document.body.style.cursor= 'default';
      	}
	},
	mounted() {
	}
}
</script>
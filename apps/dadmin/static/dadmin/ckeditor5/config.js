$(document).ready(function(){

    ClassicEditor
	.create( document.querySelector( '#id_content' ), {
				
				toolbar: {
					items: [
						'heading',
						'|',
						'fontFamily',
						'fontColor',
						'fontSize',
						'fontBackgroundColor',
						'underline',
						'strikethrough',
						'bold',
						'italic',
						'link',
						'bulletedList',
						'numberedList',
						'|',
						'outdent',
						'indent',
						'|',
						'blockQuote',
						'insertTable',
						'CKFinder',
						'imageUpload',
						'imageInsert',
						'mediaEmbed',
						'code',
						'codeBlock',
						'htmlEmbed',
						'sourceEditing',
						'undo',
						'redo',
						'|'
					]
				},
				language: 'zh-cn',
				image: {
					toolbar: [
						'imageTextAlternative',
						'imageStyle:inline',
						'imageStyle:block',
						'imageStyle:side'
					]
				},
                ckfinder: {
                    uploadUrl: '/uploads/'
                },
				table: {
					contentToolbar: [
						'tableColumn',
						'tableRow',
						'mergeTableCells'
					]
				},
					licenseKey: '',
					
					
					
				} )
				.then( editor => {
					window.editor = editor;
			
					
					
					
				} )
				.catch( error => {
					console.error( 'Oops, something went wrong!' );
					console.error( 'Please, report the following error on https://github.com/ckeditor/ckeditor5/issues with the build id and the error stack trace:' );
					console.warn( 'Build id: hbzvs8jnf1d-v5zokzbnoqws' );
					// console.error( error );
				} );



})

    


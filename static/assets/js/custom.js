
// Function to send data to the Django backend
function sendData(inputData, inputId) {
     // Make an AJAX request to the homepage (root URL) with the CSRF token
     $.ajax({
         type: 'POST',
         url: '/',  // Root URL for the homepage
         data: {'input_data': inputData, 'input_id': inputId},
         success: function(response) {
             // Handle the response from the backend
             console.log(response);

             // Update the result paragraph with the calculated result
             updateResult(response.result);
             upDateOdds(response.total_odds)
         },
         error: function(error) {
             console.error('Error:', error);
         }
     });
 }

 function upDateOdds(result){
     $('.tot_odd').each(function(){
         $(this).text(result)
     })
 }
 
 function updateResult(result) {
     var formattedResult = parseFloat(result).toLocaleString();
     $('#resultParagraph').text('Amount: ' + formattedResult);
     $('#resultParagraph2').text('Amount: ' + formattedResult);
     $('#resultParagraph3').text('Amount: ' + formattedResult);
 }

 // Set a default value for both input fields
 var defaultInputValue = 100;
 $('#inputField1').val(defaultInputValue);
 $('#inputField2').val(defaultInputValue);
 $('#inputField3').val(defaultInputValue);

 // Send data to the Django backend with the default value for both input fields
 sendData(defaultInputValue, 'inputField1');
 sendData(defaultInputValue, 'inputField2');
 sendData(defaultInputValue, 'inputField3');

 // Attach input event listener to all input fields with class "live-input"
 $('.live-input').on('input', function() {
     // Get the input value and ID
     var inputData = $(this).val();
     var inputId = $(this).attr('id');

     // Send data to the Django backend
     sendData(inputData, inputId);
 });

 $('.clickable_p').on('click', function() {
     // Get the mod_id and mod_name from the data attributes
     var stake_id = $(this).data('id');
     var stake_value = $(this).data('value');
     var stake_name = $(this).data('name');


     // Send data to the Django backend
     sendParagraphClickData(stake_id, stake_value, stake_name);
 });

 function sendParagraphClickData(stake_id, stake_value, stake_name) {
     // Make an AJAX request to the backend with the CSRF token
     $.ajax({
         type: 'POST',
         url: '/placurstak/',  // Replace with the actual URL
         data: {
             'stake_id': stake_id,
             'stake_value': stake_value,
             'stake_name': stake_name,
         },
         success: function(response) {
             // Handle the response from the backend
             if (response.result == "Authentication required"){
                 window.location.href = "login"
             }
             else{
                 fetchPlacedBets()
             }
         },
         error: function(error) {
             console.error('Error:', error);
         }
     });
 }
 $(document).ready(function() {
     // Fetch placed bets on page refresh
     fetchPlacedBets();
 });

 function fetchPlacedBets() {
     // Make an AJAX request to the backend with the CSRF token
     $.ajax({
         type: 'GET',
         url: '/get-placed-bets/',  // Replace with the actual URL
         success: function(response) {
             $('.bet_head').each(function() {
                 $(this).empty();
             });
             // Handle the response from the backend
             if (response.result){
                 $(".clickable_p").each(function(){
                     $(this).css({
                         'backgroundColor':'rgb(39,50,78)',
                     }) 
                 })
                 response.result.forEach(element => {
                     $('.bet_head').each(function() {
                         $(this).append(`
                             <div class="multiple__items">
                                 <div class="multiple__head">
                                     <div class="multiple__left">
                                         <span class="icons">
                                             <i class="fa-regular fa-futbol"></i>
                                         </span>
                                         <span class="teams_name">
                                             ${element.team1_name} vs ${element.team2_name}
                                         </span>
                                     </div>
                                     <a class="cros" onclick="sendUrl(${element.id})">
                                         <i class="fa-solid fa-xmark"></i>
                                     </a>
                                 </div>
                                 <div class="multiple__point">
                                     <span class="pbox bet_odd">
                                         ${element.odds}
                                     </span>
                                     <span class="rightname">
                                         <span class="fc bet_name">
                                             ${element.name}
                                         </span>
                                         <span class="point">
                                             1x2
                                         </span>
                                     </span>
                                 </div>
                             </div>
                         `);
                     });

                     $(".clickable_p").each(function(){
                         if (element.bet_model_id == $(this).data('id') && element.name == $(this).data('name') && element.odds == $(this).data('value')){
                             $(this).css({
                                 'backgroundColor':'rgb(255, 102, 0)',
                             })
                         }
                     })
                 });

                 $('.live-input').each(function() {
                     var inputData = $(this).val();
                     var inputId = $(this).attr('id');

                     sendData(inputData, inputId);
                 });
             }
         },
         error: function(error) {
             console.error('Error:', error);
         }
     });
 }

 function sendUrl(id){
     var elementId = id
     $.ajax({
         type: 'POST',
         url: '/deletestake/',
         data: {
             'element_id': elementId,
         },
         success: function(response) {
             fetchPlacedBets()
         },
         error: function(error) {
             console.error('Error:', error);
         }
     });
 }

 function placeBet(){
     var inputString = $('#resultParagraph')[0].innerHTML
     
     // Use regular expression to match digits and commas
     var match = inputString.match(/[0-9,]+/);

     if (match) {
         // Remove commas and convert the matched digits to a number
         var result = parseInt(match[0].replace(/,/g, ''), 10);
         if (result == 0){
             alert("Your amount is zero")
         }
         else{
             $('#pop-id').css({
                 'display': 'flex',
             })
         }
     } 
     else {
         console.log("No digits found in the input string.");
     }

 }
 function closePop(){
     $('#pop-id').css({
         'display': 'none',
     })
 }

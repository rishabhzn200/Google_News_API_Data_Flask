/**
  * Function to call the Flask API and get the data.
  *
  * @param {string} company name of the company
  * @return undefined
  *
  * @customFunction
  */
function getData(company){
  var url = 'https://sound-district-226710.appspot.com/result?companies='+company;
  Logger.log(url);
  options = {
    'method' : 'GET',
  }
  var x = 20;
  
  // Fetch the result from the Flask based API. API call directly updates the spreadsheet
  var results = UrlFetchApp.fetch(url);
  Logger.log(results);
}



/**
  * This function reads the 1st column of sheet1 and get the name of the comapnies to gather the news data for
  * and calls getData() for each of the companies listed.
  * 
  * @return undefined
  *
  * @customFunction
  */
function main(){
  
  // Step 1: Read the Sheet 1
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet1 = ss.getSheetByName('Sheet1');
  var valueMatrix = sheet1.getDataRange().getValues()
  
  // Step 2: Read the names of companies to search for
  var companies = []
  for(row=0; row<valueMatrix.length; ++row){
    companies.push(valueMatrix[row][0]);
  }
  Logger.log(companies);
  
  
  // Step 3: Run a for loop for each company to extract the data and write to the sheet
  for(idx=0; idx<companies.length; ++idx){
    var company = companies[idx];
    getData(company);
  }
}

/**
  * Function to create a trigger to update the Spreadsheet by itself
  *
  * 
  * @return undefined
  *
  * @customFunction
  */
function createTrigger() {
  
  // Trigger every 1 minute
  ScriptApp.newTrigger('timeTrigger')
      .timeBased()
      .everyMinutes(1)
      .create();
}


/**
  * Function to limit the maximum number of updates to prevent the trigger running indefinitely
  *
  * @return undefined
  *
  * @customFunction
  */
function timeTrigger(){
  var userProperties = PropertiesService.getUserProperties();
  var loopCounter = Number(userProperties.getProperty('loopCounter'));
  
  // Max updates to the spreadsheet using trigger
  var maxCounterVal = 3;
  
  if (loopCounter < maxCounterVal) {
    Logger.log("Running loop " + loopCounter);
    
    // Call the main function
    main()
    
    // Increment the properties service counter for the loop
    loopCounter +=1;
    userProperties.setProperty('loopCounter', loopCounter);
  }
  else {
    // Log message to confirm loop is finished
    Logger.log("Finished");
    deleteTrigger();  
  }
}


/**
  * Function to delete all the triggers
  *
  * @return undefined
  *
  * @customFunction
  */
function deleteTrigger() {
  
  // Loop over all triggers and delete them
  var allTriggers = ScriptApp.getProjectTriggers();
  
  for (var i = 0; i < allTriggers.length; i++) {
    ScriptApp.deleteTrigger(allTriggers[i]);
  }
}


/**
  * Function to test the functionality of getData
  *
  * @return undefined
  *
  * @customFunction
  */
function test(){
  getData('Facebook');
}
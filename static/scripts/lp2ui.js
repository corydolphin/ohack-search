/*
 * Launchpad2 user-interface code
 * Written by Jeffrey Stanton (Olin 2010) http://nomagicsmoke.com/
 * Inspired by work by Gregory Marra (Olin 2010)
 * This software uses JQuery, licensed under the BSD license.
 */
 
/*************** BSD LICENSE *****************

Copyright (c) 2010, Jeffrey Stanton
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice, this
  list of conditions and the following disclaimer in the documentation and/or
  other materials provided with the distribution.

* Neither the name of JEFFREY STANTON nor the names of LAUNCHPAD2's contributors
  may be used to endorse or promote products derived from this software without
  specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

*/

var appList;
var matchedApps = [];

var getName = function(app){
	return $(app).children('span').text();
	}



/** document.ready runs when page loads.  Main UI code  */
$(document).ready(function(){

var appNameFilter = $('#appName');
var apps = $("#appList a");
matchedApps = apps;

$('#filterForm').submit(function(){
	if(matchedApps.length>=1){
		var link = apps[matchedApps[0]];
		document.location.href = $(link).attr('href');
		return false;
		}
	return false;
	});
appNameFilter.change(function(){
	var query = appNameFilter.val().toLowerCase();
	var queryParts = query.split(" ");
	//check each app to see if it matches user search terms
	matchedApps = [];
	apps.each(function(index){
		var app = $(apps[index]);
		var name = getName(app).toLowerCase();
		var matched = true;
		for(partIndex in queryParts){
			var queryTerm = queryParts[partIndex];
			if(name.indexOf(queryTerm)<0){ //app name didnt have one of the query terms
				matched = false;
				break;
				}
			}
		if(matched){
			app.show();
			matchedApps.push(index);
		}else{
			app.hide();
			}
		});
	if(matchedApps.length>=1){
		$('#singleResultName').text(getName(apps[matchedApps[0]]));
		$('#singleReminder').show();
	}else{
		$('#singleReminder').hide();
		}
	});
appNameFilter.focus(function(){
	$('#singleReminder').show();
	});
appNameFilter.blur(function(){
	$('#singleReminder').hide();
	});

//$('#singleReminder').hide();
appNameFilter.keyup(function(e){ appNameFilter.change(); });
appNameFilter.focus();
appNameFilter.select();
appNameFilter.change();

});
/** end of document.ready() function */

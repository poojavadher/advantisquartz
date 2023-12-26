

frappe.pages['form-d-attendance-re'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'FORM D Attendance Register',
		single_column: true
	});



	let fields = [
		{
			label: 'Month',
			fieldtype: 'Select',
			fieldname: 'month',
			options: "\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember"
		},
		{
			label: 'Year',
			fieldtype: 'Select',
			fieldname: 'year',
			options: getYearOptions()
		},
	];



	function getYearOptions() {
		let currentYear = new Date().getFullYear();
		let yearOptions = "";
		for (let i = currentYear; i >= currentYear - 0; i--) {
			"\n" + (yearOptions += i);
		}
		return yearOptions;
	}

	let monthsDictionary = {
		'January': '01',
		'February': '02',
		'March': '03',
		'April': '04',
		'May': '05',
		'June': '06',
		'July': '07',
		'August': '08',
		'September': '09',
		'October': '10',
		'November': '11',
		'December': '12'
	};

	var data;
	var year = null;
	var selectedMonth = null;
	var monthValue = null;
	wrapper.page.set_primary_action('Print', function () {
		window.print()
	});

	wrapper.page.set_primary_action('Print', function () {
		var style = document.createElement('style');
		style.textContent = '@media print { .page-head{ display:none;} .page-body{margin-top:3rem}}';
		document.head.appendChild(style);
		window.print();
	});

	fields.forEach(field => {
		let dateField = page.add_field(field);
		dateField.$input.on('change', function () {
			if (field.fieldname === 'month') {
				selectedMonth = dateField.get_value();
				monthValue = monthsDictionary[selectedMonth];
				console.log("Month selected:", selectedMonth, "Value:", monthValue);
			}
			if (field.fieldname === 'year') {
				year = dateField.get_value();
				console.log("Year selected:", year);
			}
			if (monthValue && year) {
				// page.clear_primary_action();
				// page.clear_menu();
				// page.fields_dict = {};
				// page.fields = [];
				// page.body.empty();
				page.body.empty();
				frappe.call({
					method: 'advantisquartz.advantisquartz.page.form_d_attendance_re.form_d_attendance_re.get_attendance',
					args: {
						month: monthValue,
						year: year
					},
					callback: function (response) {
						data = response.message;
						// console.log(data);
						getData(data)
					}
				});
			}
		});
	});


	function getData(data) {

		var employeeNames = Object.keys(data || {});

		var firstMinTimes = {};
		var firstMaxTimes = {};
		var secondMinTimes = {};
		var secondMaxTimes = {};
		var thirdMinTimes = {};
		var thirdMaxTimes = {};
		var fourthMinTimes = {};
		var fourthMaxTimes = {};
		var fifthMinTimes = {};
		var fifthMaxTimes = {};
		var sixthMinTimes = {};
		var sixthMaxTimes = {};
		var seventhMinTimes = {};
		var seventhMaxTimes = {};
		var eighthMinTimes = {};
		var eighthMaxTimes = {};
		var ninthMinTimes = {};
		var ninthMaxTimes = {};
		var tenthMinTimes = {};
		var tenthMaxTimes = {};
		var elevenMinTimes = {};
		var elevenMaxTimes = {};
		var twelveMinTimes = {};
		var twelveMaxTimes = {};
		var thirteenMinTimes = {};
		var thirteenMaxTimes = {};
		var fourteenMinTimes = {};
		var fourteenMaxTimes = {};
		var fifteenMinTimes = {};
		var fifteenMaxTimes = {};
		var sixteenMinTimes = {};
		var sixteenMaxTimes = {};
		var seventeenMinTimes = {};
		var seventeenMaxTimes = {};
		var eighteenMinTimes = {};
		var eighteenMaxTimes = {};
		var nineteenMinTimes = {};
		var nineteenMaxTimes = {};
		var twentyMinTimes = {};
		var twentyMaxTimes = {};
		var twentyoneMinTimes = {};
		var twentyoneMaxTimes = {};
		var twentytwoMinTimes = {};
		var twentytwoMaxTimes = {};
		var twentythreeMinTimes = {};
		var twentythreeMaxTimes = {};
		var twentyfourMinTimes = {};
		var twentyfourMaxTimes = {};
		var twentyfiveMinTimes = {};
		var twentyfiveMaxTimes = {};
		var twentysixMinTimes = {};
		var twentysixMaxTimes = {};
		var twentysevenMinTimes = {};
		var twentysevenMaxTimes = {};
		var twentyeightMinTimes = {};
		var twentyeightMaxTimes = {};
		var twentynineMinTimes = {};
		var twentynineMaxTimes = {};
		var thirtyMinTimes = {};
		var thirtyMaxTimes = {};
		var thirtyoneMinTimes = {};
		var thirtyoneMaxTimes = {};



		employeeNames.forEach(function (employeeName) {
			var first = Object.keys(data[employeeName])[0];
			var firstData = data[employeeName][first];

			if (firstData && firstData.IN && firstData.IN.Mintime) {
				var firstmintime = firstData.IN.Mintime;
				firstMinTimes[employeeName] = firstmintime;
			}
			if (firstData && firstData.OUT && firstData.OUT.Maxtime) {
				var firstmaxtime = firstData.OUT.Maxtime;
				firstMaxTimes[employeeName] = firstmaxtime;
			}

			var second = Object.keys(data[employeeName])[1];
			var secondData = data[employeeName][second];

			if (secondData && secondData.IN && secondData.IN.Mintime) {
				var secondmintime = secondData.IN.Mintime;
				secondMinTimes[employeeName] = secondmintime;
			}
			if (secondData && secondData.OUT && secondData.OUT.Maxtime) {
				var secondmaxtime = secondData.OUT.Maxtime;
				secondMaxTimes[employeeName] = secondmaxtime;
			}


			var third = Object.keys(data[employeeName])[2];
			var thirdData = data[employeeName][third];

			if (thirdData && thirdData.IN && thirdData.IN.Mintime) {
				var thirdmintime = thirdData.IN.Mintime;
				thirdMinTimes[employeeName] = thirdmintime;
			}
			if (thirdData && thirdData.OUT && thirdData.OUT.Maxtime) {
				var thirdmaxtime = thirdData.OUT.Maxtime;
				thirdMaxTimes[employeeName] = thirdmaxtime;
			}


			var fourth = Object.keys(data[employeeName])[3];
			var fourthData = data[employeeName][fourth];

			if (fourthData && fourthData.IN && fourthData.IN.Mintime) {
				var fourthmintime = fourthData.IN.Mintime;
				fourthMinTimes[employeeName] = fourthmintime;
			}
			if (fourthData && fourthData.OUT && fourthData.OUT.Maxtime) {
				var fourthmaxtime = fourthData.OUT.Maxtime;
				fourthMaxTimes[employeeName] = fourthmaxtime;
			}


			var fifth = Object.keys(data[employeeName])[4];
			var fifthData = data[employeeName][fifth];

			if (fifthData && fifthData.IN && fifthData.IN.Mintime) {
				var fifthmintime = fifthData.IN.Mintime;
				fifthMinTimes[employeeName] = fifthmintime;
			}
			if (fifthData && fifthData.OUT && fifthData.OUT.Maxtime) {
				var fifthmaxtime = fifthData.OUT.Maxtime;
				fifthMaxTimes[employeeName] = fifthmaxtime;
			}


			var sixth = Object.keys(data[employeeName])[5];
			var sixthData = data[employeeName][sixth];

			if (sixthData && sixthData.IN && sixthData.IN.Mintime) {
				var sixthmintime = sixthData.IN.Mintime;
				sixthMinTimes[employeeName] = sixthmintime;
			}
			if (sixthData && sixthData.OUT && sixthData.OUT.Maxtime) {
				var sixthmaxtime = sixthData.OUT.Maxtime;
				sixthMaxTimes[employeeName] = sixthmaxtime;
			}


			var seventh = Object.keys(data[employeeName])[6];
			var seventhData = data[employeeName][seventh];

			if (seventhData && seventhData.IN && seventhData.IN.Mintime) {
				var seventhmintime = seventhData.IN.Mintime;
				seventhMinTimes[employeeName] = seventhmintime;
			}
			if (seventhData && seventhData.OUT && seventhData.OUT.Maxtime) {
				var seventhmaxtime = seventhData.OUT.Maxtime;
				seventhMaxTimes[employeeName] = seventhmaxtime;
			}


			var eighth = Object.keys(data[employeeName])[7];
			var eighthData = data[employeeName][eighth];

			if (eighthData && eighthData.IN && eighthData.IN.Mintime) {
				var eighthmintime = eighthData.IN.Mintime;
				eighthMinTimes[employeeName] = eighthmintime;
			}
			if (eighthData && eighthData.OUT && eighthData.OUT.Maxtime) {
				var eighthmaxtime = eighthData.OUT.Maxtime;
				eighthMaxTimes[employeeName] = eighthmaxtime;
			}


			var ninth = Object.keys(data[employeeName])[8];
			var ninthData = data[employeeName][ninth];

			if (ninthData && ninthData.IN && ninthData.IN.Mintime) {
				var ninthmintime = ninthData.IN.Mintime;
				ninthMinTimes[employeeName] = ninthmintime;
			}
			if (ninthData && ninthData.OUT && ninthData.OUT.Maxtime) {
				var ninthmaxtime = ninthData.OUT.Maxtime;
				ninthMaxTimes[employeeName] = ninthmaxtime;
			}


			var tenth = Object.keys(data[employeeName])[9];
			var tenthData = data[employeeName][tenth];

			if (tenthData && tenthData.IN && tenthData.IN.Mintime) {
				var tenthmintime = tenthData.IN.Mintime;
				tenthMinTimes[employeeName] = tenthmintime;
			}
			if (tenthData && tenthData.OUT && tenthData.OUT.Maxtime) {
				var tenthmaxtime = tenthData.OUT.Maxtime;
				tenthMaxTimes[employeeName] = tenthmaxtime;
			}


			var eleven = Object.keys(data[employeeName])[10];
			var elevenData = data[employeeName][eleven];

			if (elevenData && elevenData.IN && elevenData.IN.Mintime) {
				var elevenmintime = elevenData.IN.Mintime;
				elevenMinTimes[employeeName] = elevenmintime;
			}
			if (elevenData && elevenData.OUT && elevenData.OUT.Maxtime) {
				var elevenmaxtime = elevenData.OUT.Maxtime;
				elevenMaxTimes[employeeName] = elevenmaxtime;
			}


			var twelve = Object.keys(data[employeeName])[11];
			var twelveData = data[employeeName][twelve];

			if (twelveData && twelveData.IN && twelveData.IN.Mintime) {
				var twelvemintime = twelveData.IN.Mintime;
				twelveMinTimes[employeeName] = twelvemintime;
			}
			if (twelveData && twelveData.OUT && twelveData.OUT.Maxtime) {
				var twelvemaxtime = twelveData.OUT.Maxtime;
				twelveMaxTimes[employeeName] = twelvemaxtime;
			}


			var thirteen = Object.keys(data[employeeName])[12];
			var thirteenData = data[employeeName][thirteen];

			if (thirteenData && thirteenData.IN && thirteenData.IN.Mintime) {
				var thirteenmintime = thirteenData.IN.Mintime;
				thirteenMinTimes[employeeName] = thirteenmintime;
			}
			if (thirteenData && thirteenData.OUT && thirteenData.OUT.Maxtime) {
				var thirteenmaxtime = thirteenData.OUT.Maxtime;
				thirteenMaxTimes[employeeName] = thirteenmaxtime;
			}


			var fourteen = Object.keys(data[employeeName])[13];
			var fourteenData = data[employeeName][fourteen];

			if (fourteenData && fourteenData.IN && fourteenData.IN.Mintime) {
				var fourteenmintime = fourteenData.IN.Mintime;
				fourteenMinTimes[employeeName] = fourteenmintime;
			}
			if (fourteenData && fourteenData.OUT && fourteenData.OUT.Maxtime) {
				var fourteenmaxtime = fourteenData.OUT.Maxtime;
				fourteenMaxTimes[employeeName] = fourteenmaxtime;
			}


			var fifteen = Object.keys(data[employeeName])[14];
			var fifteenData = data[employeeName][fifteen];

			if (fifteenData && fifteenData.IN && fifteenData.IN.Mintime) {
				var fifteenmintime = fifteenData.IN.Mintime;
				fifteenMinTimes[employeeName] = fifteenmintime;
			}
			if (fifteenData && fifteenData.OUT && fifteenData.OUT.Maxtime) {
				var fifteenmaxtime = fifteenData.OUT.Maxtime;
				fifteenMaxTimes[employeeName] = fifteenmaxtime;
			}


			var sixteen = Object.keys(data[employeeName])[15];
			var sixteenData = data[employeeName][sixteen];

			if (sixteenData && sixteenData.IN && sixteenData.IN.Mintime) {
				var sixteenmintime = sixteenData.IN.Mintime;
				sixteenMinTimes[employeeName] = sixteenmintime;
			}
			if (sixteenData && sixteenData.OUT && sixteenData.OUT.Maxtime) {
				var sixteenmaxtime = sixteenData.OUT.Maxtime;
				sixteenMaxTimes[employeeName] = sixteenmaxtime;
			}


			var seventeen = Object.keys(data[employeeName])[16];
			var seventeenData = data[employeeName][seventeen];

			if (seventeenData && seventeenData.IN && seventeenData.IN.Mintime) {
				var seventeenmintime = seventeenData.IN.Mintime;
				seventeenMinTimes[employeeName] = seventeenmintime;
			}
			if (seventeenData && seventeenData.OUT && seventeenData.OUT.Maxtime) {
				var seventeenmaxtime = seventeenData.OUT.Maxtime;
				seventeenMaxTimes[employeeName] = seventeenmaxtime;
			}


			var eighteen = Object.keys(data[employeeName])[17];
			var eighteenData = data[employeeName][eighteen];

			if (eighteenData && eighteenData.IN && eighteenData.IN.Mintime) {
				var eighteenmintime = eighteenData.IN.Mintime;
				eighteenMinTimes[employeeName] = eighteenmintime;
			}
			if (eighteenData && eighteenData.OUT && eighteenData.OUT.Maxtime) {
				var eighteenmaxtime = eighteenData.OUT.Maxtime;
				eighteenMaxTimes[employeeName] = eighteenmaxtime;
			}


			var nineteen = Object.keys(data[employeeName])[18];
			var nineteenData = data[employeeName][nineteen];

			if (nineteenData && nineteenData.IN && nineteenData.IN.Mintime) {
				var nineteenmintime = nineteenData.IN.Mintime;
				nineteenMinTimes[employeeName] = nineteenmintime;
			}
			if (nineteenData && nineteenData.OUT && nineteenData.OUT.Maxtime) {
				var nineteenmaxtime = nineteenData.OUT.Maxtime;
				nineteenMaxTimes[employeeName] = nineteenmaxtime;
			}


			var twenty = Object.keys(data[employeeName])[19];
			var twentyData = data[employeeName][twenty];

			if (twentyData && twentyData.IN && twentyData.IN.Mintime) {
				var twentymintime = twentyData.IN.Mintime;
				twentyMinTimes[employeeName] = twentymintime;
			}
			if (twentyData && twentyData.OUT && twentyData.OUT.Maxtime) {
				var twentymaxtime = twentyData.OUT.Maxtime;
				twentyMaxTimes[employeeName] = twentymaxtime;
			}


			var twentyone = Object.keys(data[employeeName])[20];
			var twentyoneData = data[employeeName][twentyone];

			if (twentyoneData && twentyoneData.IN && twentyoneData.IN.Mintime) {
				var twentyonemintime = twentyoneData.IN.Mintime;
				twentyoneMinTimes[employeeName] = twentyonemintime;
			}
			if (twentyoneData && twentyoneData.OUT && twentyoneData.OUT.Maxtime) {
				var twentyonemaxtime = twentyoneData.OUT.Maxtime;
				twentyoneMaxTimes[employeeName] = twentyonemaxtime;
			}


			var twentytwo = Object.keys(data[employeeName])[21];
			var twentytwoData = data[employeeName][twentytwo];

			if (twentytwoData && twentytwoData.IN && twentytwoData.IN.Mintime) {
				var twentytwomintime = twentytwoData.IN.Mintime;
				twentytwoMinTimes[employeeName] = twentytwomintime;
			}
			if (twentytwoData && twentytwoData.OUT && twentytwoData.OUT.Maxtime) {
				var twentytwomaxtime = twentytwoData.OUT.Maxtime;
				twentytwoMaxTimes[employeeName] = twentytwomaxtime;
			}


			var twentythree = Object.keys(data[employeeName])[22];
			var twentythreeData = data[employeeName][twentythree];

			if (twentythreeData && twentythreeData.IN && twentythreeData.IN.Mintime) {
				var twentythreemintime = twentythreeData.IN.Mintime;
				twentythreeMinTimes[employeeName] = twentythreemintime;
			}
			if (twentythreeData && twentythreeData.OUT && twentythreeData.OUT.Maxtime) {
				var twentythreemaxtime = twentythreeData.OUT.Maxtime;
				twentythreeMaxTimes[employeeName] = twentythreemaxtime;
			}


			var twentyfour = Object.keys(data[employeeName])[23];
			var twentyfourData = data[employeeName][twentyfour];

			if (twentyfourData && twentyfourData.IN && twentyfourData.IN.Mintime) {
				var twentyfourmintime = twentyfourData.IN.Mintime;
				twentyfourMinTimes[employeeName] = twentyfourmintime;
			}
			if (twentyfourData && twentyfourData.OUT && twentyfourData.OUT.Maxtime) {
				var twentyfourmaxtime = twentyfourData.OUT.Maxtime;
				twentyfourMaxTimes[employeeName] = twentyfourmaxtime;
			}


			var twentyfive = Object.keys(data[employeeName])[24];
			var twentyfiveData = data[employeeName][twentyfive];

			if (twentyfiveData && twentyfiveData.IN && twentyfiveData.IN.Mintime) {
				var twentyfivemintime = twentyfiveData.IN.Mintime;
				twentyfiveMinTimes[employeeName] = twentyfivemintime;
			}
			if (twentyfiveData && twentyfiveData.OUT && twentyfiveData.OUT.Maxtime) {
				var twentyfivemaxtime = twentyfiveData.OUT.Maxtime;
				twentyfiveMaxTimes[employeeName] = twentyfivemaxtime;
			}


			var twentysix = Object.keys(data[employeeName])[25];
			var twentysixData = data[employeeName][twentysix];

			if (twentysixData && twentysixData.IN && twentysixData.IN.Mintime) {
				var twentysixmintime = twentysixData.IN.Mintime;
				twentysixMinTimes[employeeName] = twentysixmintime;
			}
			if (twentysixData && twentysixData.OUT && twentysixData.OUT.Maxtime) {
				var twentysixmaxtime = twentysixData.OUT.Maxtime;
				twentysixMaxTimes[employeeName] = twentysixmaxtime;
			}


			var twentyseven = Object.keys(data[employeeName])[26];
			var twentysevenData = data[employeeName][twentyseven];

			if (twentysevenData && twentysevenData.IN && twentysevenData.IN.Mintime) {
				var twentysevenmintime = twentysevenData.IN.Mintime;
				twentysevenMinTimes[employeeName] = twentysevenmintime;
			}
			if (twentysevenData && twentysevenData.OUT && twentysevenData.OUT.Maxtime) {
				var twentysevenmaxtime = twentysevenData.OUT.Maxtime;
				twentysevenMaxTimes[employeeName] = twentysevenmaxtime;
			}


			var twentyeight = Object.keys(data[employeeName])[27];
			var twentyeightData = data[employeeName][twentyeight];

			if (twentyeightData && twentyeightData.IN && twentyeightData.IN.Mintime) {
				var twentyeightmintime = twentyeightData.IN.Mintime;
				twentyeightMinTimes[employeeName] = twentyeightmintime;
			}
			if (twentyeightData && twentyeightData.OUT && twentyeightData.OUT.Maxtime) {
				var twentyeightmaxtime = twentyeightData.OUT.Maxtime;
				twentyeightMaxTimes[employeeName] = twentyeightmaxtime;
			}


			var twentynine = Object.keys(data[employeeName])[28];
			var twentynineData = data[employeeName][twentynine];

			if (twentynineData && twentynineData.IN && twentynineData.IN.Mintime) {
				var twentyninemintime = twentynineData.IN.Mintime;
				twentynineMinTimes[employeeName] = twentyninemintime;
			}
			if (twentynineData && twentynineData.OUT && twentynineData.OUT.Maxtime) {
				var twentyninemaxtime = twentynineData.OUT.Maxtime;
				twentynineMaxTimes[employeeName] = twentyninemaxtime;
			}


			var thirty = Object.keys(data[employeeName])[29];
			var thirtyData = data[employeeName][thirty];

			if (thirtyData && thirtyData.IN && thirtyData.IN.Mintime) {
				var thirtymintime = thirtyData.IN.Mintime;
				thirtyMinTimes[employeeName] = thirtymintime;
			}
			if (thirtyData && thirtyData.OUT && thirtyData.OUT.Maxtime) {
				var thirtymaxtime = thirtyData.OUT.Maxtime;
				thirtyMaxTimes[employeeName] = thirtymaxtime;
			}


			var thirtyone = Object.keys(data[employeeName])[30];
			var thirtyoneData = data[employeeName][thirtyone];

			if (thirtyoneData && thirtyoneData.IN && thirtyoneData.IN.Mintime) {
				var thirtyonemintime = thirtyoneData.IN.Mintime;
				thirtyoneMinTimes[employeeName] = thirtyonemintime;
			}
			if (thirtyoneData && thirtyoneData.OUT && thirtyoneData.OUT.Maxtime) {
				var thirtyonemaxtime = thirtyoneData.OUT.Maxtime;
				thirtyoneMaxTimes[employeeName] = thirtyonemaxtime;
			}



		});

		renderTable(employeeNames, firstMinTimes, firstMaxTimes, secondMinTimes, secondMaxTimes, thirdMinTimes, thirdMaxTimes, fourthMinTimes, fourthMaxTimes, fifthMinTimes, fifthMaxTimes, sixthMinTimes, sixthMaxTimes, seventhMinTimes, seventhMaxTimes, eighthMinTimes, eighthMaxTimes, ninthMinTimes, ninthMaxTimes, tenthMinTimes, tenthMaxTimes, elevenMinTimes, elevenMaxTimes, twelveMinTimes, twelveMaxTimes, thirteenMinTimes, thirteenMaxTimes, fourteenMinTimes, fourteenMaxTimes, fifteenMinTimes, fifteenMaxTimes, sixteenMinTimes, sixteenMaxTimes, seventeenMinTimes, seventeenMaxTimes, eighteenMinTimes, eighteenMaxTimes, nineteenMinTimes, nineteenMaxTimes, twentyMinTimes, twentyMaxTimes, twentyoneMinTimes, twentyoneMaxTimes, twentytwoMinTimes, twentytwoMaxTimes, twentythreeMinTimes, twentythreeMaxTimes, twentyfourMinTimes, twentyfourMaxTimes, twentyfiveMinTimes, twentyfiveMaxTimes, twentysixMinTimes, twentysixMaxTimes, twentysevenMinTimes, twentysevenMaxTimes, twentyeightMinTimes, twentyeightMaxTimes, twentynineMinTimes, twentynineMaxTimes, thirtyMinTimes, thirtyMaxTimes, thirtyoneMinTimes, thirtyoneMaxTimes);
	}




	function renderTable(employeeNames, firstMinTimes, firstMaxTimes, secondMinTimes, secondMaxTimes, thirdMinTimes, thirdMaxTimes, fourthMinTimes, fourthMaxTimes, fifthMinTimes, fifthMaxTimes, sixthMinTimes, sixthMaxTimes, seventhMinTimes, seventhMaxTimes, eighthMinTimes, eighthMaxTimes, ninthMinTimes, ninthMaxTimes, tenthMinTimes, tenthMaxTimes, elevenMinTimes, elevenMaxTimes, twelveMinTimes, twelveMaxTimes, thirteenMinTimes, thirteenMaxTimes, fourteenMinTimes, fourteenMaxTimes, fifteenMinTimes, fifteenMaxTimes, sixteenMinTimes, sixteenMaxTimes, seventeenMinTimes, seventeenMaxTimes, eighteenMinTimes, eighteenMaxTimes, nineteenMinTimes, nineteenMaxTimes, twentyMinTimes, twentyMaxTimes, twentyoneMinTimes, twentyoneMaxTimes, twentytwoMinTimes, twentytwoMaxTimes, twentythreeMinTimes, twentythreeMaxTimes, twentyfourMinTimes, twentyfourMaxTimes, twentyfiveMinTimes, twentyfiveMaxTimes, twentysixMinTimes, twentysixMaxTimes, twentysevenMinTimes, twentysevenMaxTimes, twentyeightMinTimes, twentyeightMaxTimes, twentynineMinTimes, twentynineMaxTimes, thirtyMinTimes, thirtyMaxTimes, thirtyoneMinTimes, thirtyoneMaxTimes) {
		$(frappe.render_template("form_d_attendance_re", {
			month: selectedMonth,
			year: year,
			names: employeeNames,
			first_min: firstMinTimes,
			first_max: firstMaxTimes,
			second_min: secondMinTimes,
			second_max: secondMaxTimes,
			third_min: thirdMinTimes,
			third_max: thirdMaxTimes,
			fourth_min: fourthMinTimes,
			fourth_max: fourthMaxTimes,
			fifth_min: fifthMinTimes,
			fifth_max: fifthMaxTimes,
			sixth_min: sixthMinTimes,
			sixth_max: sixthMaxTimes,
			seventh_min: seventhMinTimes,
			seventh_max: seventhMaxTimes,
			eighth_min: eighthMinTimes,
			eighth_max: eighthMaxTimes,
			ninth_min: ninthMinTimes,
			ninth_max: ninthMaxTimes,
			tenth_min: tenthMinTimes,
			tenth_max: tenthMaxTimes,
			eleventh_min: elevenMinTimes,
			eleventh_max: elevenMaxTimes,
			twelve_min: twelveMinTimes,
			twelve_max: twelveMaxTimes,
			thirteen_min: thirteenMinTimes,
			thirteen_max: thirteenMaxTimes,
			fourteen_min: fourteenMinTimes,
			fourteen_max: fourteenMaxTimes,
			fifteen_min: fifteenMinTimes,
			fifteen_max: fifteenMaxTimes,
			sixteen_min: sixteenMinTimes,
			sixteen_max: sixteenMaxTimes,
			seventeen_min: seventeenMinTimes,
			seventeen_max: seventeenMaxTimes,
			eighteen_min: eighteenMinTimes,
			eighteen_max: eighteenMaxTimes,
			ninteen_min: nineteenMinTimes,
			ninteen_max: nineteenMaxTimes,
			twenty_min: twentyMinTimes,
			twenty_max: twentyMaxTimes,
			twentyone_min: twentyoneMinTimes,
			twentyone_max: twentyoneMaxTimes,
			twentytwo_min: twentytwoMinTimes,
			twentytwo_max: twentytwoMaxTimes,
			twentythree_min: twentythreeMinTimes,
			twentythree_max: twentythreeMaxTimes,
			twentyfour_min: twentyfourMinTimes,
			twentyfour_max: twentyfourMaxTimes,
			twentyfive_min: twentyfiveMinTimes,
			twentyfive_max: twentyfiveMaxTimes,
			twentysix_min: twentysixMinTimes,
			twentysix_max: twentysixMaxTimes,
			twentyseven_min: twentysevenMinTimes,
			twentyseven_max: twentysevenMaxTimes,
			twentyeight_min: twentyeightMinTimes,
			twentyeight_max: twentyeightMaxTimes,
			twentynine_min: twentynineMinTimes,
			twentynine_max: twentynineMaxTimes,
			thirty_min: thirtyMinTimes,
			thirty_max: thirtyMaxTimes,
			thirtyone_min: thirtyoneMinTimes,
			thirtyone_max: thirtyoneMaxTimes
		})).appendTo(page.body);
	}
}





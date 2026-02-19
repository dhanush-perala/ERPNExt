document.write(` <link href="/media_isro/image/favicon.png.webp" rel="icon">
  <link href="assets/style.css" rel="stylesheet">
  <style>
#searchidM {display: none;}
#searchidD {display: inline-block;}
@media screen and (max-width: 990px) {
#searchidD {display: none;}
#searchidM {display: inline-block;}
.navbar { width: 100%; }

#topbar { min-height: 0px; height: 0px; }
.bannerStyle { width: 1600px;}

}
</style>
</head>
<body onload="renderTimelineBackBtn()" onresize="menuResize()">
  <script src="header/accessibility.js"></script>
  <script src="header/navigation.js"></script>
  <script> 
    function goToOtherLanguage(){
      var currentUrl = window.location.href;
      var targetUrl="";
      if (!currentUrl.includes("ISRO_HINDI")){ //It is an English page
          if (currentUrl.includes("\/ISRO_EN\/")){
            targetUrl = currentUrl.replace("ISRO_EN","ISRO_HINDI");
          }else if (currentUrl.includes("\/ISRO_DEP\/")){
            targetUrl = currentUrl.replace("ISRO_DEP","ISRO_HINDI_DEP");
          }else if (!currentUrl.includes(".html")){ 
            //it's the index page in English e.g. https://www.isro.gov.in
            targetUrl = currentUrl+"/ISRO_HINDI";
          }else{
            //there is .html e.g. https://www.isro.gov.in/xyz.html
            var lastSlashIndex = currentUrl.lastIndexOf("\/");
            var substr1 = currentUrl.substring(0,lastSlashIndex+1);
            var substr2 = currentUrl.substring(lastSlashIndex+1,currentUrl.length);
            targetUrl = substr1+"ISRO_HINDI\/"+substr2;
          }
      }else {
        if (currentUrl.includes("\/ISRO_HINDI\/"))
          targetUrl = currentUrl.replace("ISRO_HINDI","ISRO_EN");
          else if (currentUrl.includes("\/ISRO_HINDI_DEP\/"))
          targetUrl = currentUrl.replace("ISRO_HINDI_DEP","ISRO_DEP");
        }
        window.location.assign(targetUrl);
        return false;
      }
    function renderTimelineBackBtn(){
      var currentUrl = window.location.href;
      if (currentUrl.includes("?timeline=timeline"))
        document.getElementById("timeLineBackBtn").style.visibility='visible';
      if(window.innerWidth < 991 ){
        document.getElementById("navbar").classList.remove('navbar');
        document.getElementById("navbar").classList.add('navbar');
        document.getElementById("menu").classList.remove('navbar');
        document.getElementById("menu").classList.remove('navbar1');
      }else{
        document.getElementById("navbar").classList.remove('navbar');
        document.getElementById("menu").classList.remove('navbar');
        document.getElementById("menu").classList.add('navbar');
        document.getElementById("menu").classList.add('navbar1');
      }
      document.getElementById("searchTextM").addEventListener('keyup', function onEvent(e) {
        if (e.keyCode === 13) 
       { 
       searchTextM();
        }
       });
       
       document.getElementById("searchTextD").addEventListener('keyup', function onEvent(e) {
        if (e.keyCode === 13) 
       {
       searchTextD(); 
       }
       });
    }
    function menuResize(){
      if(window.innerWidth < 991 ){
        document.getElementById("navbar").classList.remove('navbar');
        document.getElementById("navbar").classList.add('navbar');
        document.getElementById("menu").classList.remove('navbar');
        document.getElementById("menu").classList.remove('navbar1');
        document.getElementById("dotsID").style.display = "block";
//07012025
        if(document.getElementById("mobileNavToggleISRO").classList.contains("bi-x"))
        {
          document.getElementById("dotsID").style.display = "none";
          document.getElementById("searchidM").style.display = "none";
        }
        else if(document.getElementById("mobileNavToggleISRO").classList.contains("bi-list"))
        {
          document.getElementById("searchidM").style.display = "block";
        }
  //07012025 end
      }else{
        document.getElementById("navbar").classList.remove('navbar');
        document.getElementById("menu").classList.remove('navbar');
        document.getElementById("menu").classList.add('navbar');
        document.getElementById("menu").classList.add('navbar1');
       document.getElementById("dotsID").style.display = "none";
       document.getElementById("searchidM").style.display = "none";   //070125
      }
    }
  </script>
  <script>



function searchTextM() {
var searchtextM = document.getElementById("searchTextM").value;
//alert(searchtext);
if(searchtextM == "") {
document.getElementById("searchTextM").style.background = "#ffc9c9";
document.getElementById("searchTextM").placeholder = "Enter Keyword";
} else {
location.href = 'search.html#gsc.q='+searchtextM;
} }

function searchTextD() {
var searchtextD = document.getElementById("searchTextD").value;
//alert(searchtext);
if(searchtextD == "") {
document.getElementById("searchTextD").style.background = "#ffc9c9";
document.getElementById("searchTextD").placeholder = "Enter Keyword";
} else {
document.getElementById("searchTextD").style.border = "none";
location.href = 'search.html#gsc.q='+searchtextD;
} }



</script>

    <div id="topbar" class="d-flex align-items-center fixed-top">
    <div class="container d-flex justify-content-center justify-content-md-between">
      <div class="languages d-none d-md-flex align-items-center">
        <ul class="topNavBar">
          <li><a tabIndex="0" href="https://www.isro.gov.in/" title="English" class="English" >English</a></li>
          <li>|</li>
          <li><a tabIndex="0" style="cursor:pointer;" onclick="goToOtherLanguage();" class="Hindi" title="Hindi" >हिंदी</a></li>
          <li>|</li>  
          <li><a href="Sitemap.html" class="English" title="Sitemap" >Sitemap</a></li>
          <li>|</li>
          <li><a href="contact.html"  title="Contact Us" >Contact us</a></li>
          <li>|</li>
          <li><a href="https://www.isro.gov.in/ISROAPP/fFBF" target="_blank" rel="noopener noreferrer" title="Feedback">Feedback</a></li>
          <li>|</li>
          <li><a href="RTI.html" title="RTI" >RTI</a></li>
          <li>|</li>
          <li><a href="Careers.html" title="Career">Career</a></li>
          <li>|</li>
          <li><a href="Tenders.html" title="Tender">Tender</a></li> 
          <li>|</li>
          <li><a href="FAQ.html" title="FAQ">FAQ</a></li>          
        </ul>
      </div>
      <div class="languages d-none d-md-flex align-items-center">
        <ul><li><a href="https://www.facebook.com/ISRO" target="_blank" rel="noopener noreferrer"  onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')"class="facebook" title="Facebook"><i class="bx bxl-facebook"></i></a></li>
          <li><a href="https://twitter.com/isro" target="_blank" rel="noopener noreferrer"  onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')" class="twitter bx" title="X"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="13" fill="currentColor"  viewBox="0 3 16 16">
          <path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865l8.875 11.633Z"/>
        </svg></a></li>
          <li><a href="https://www.youtube.com/channel/UCw5hEVOTfz_AfzsNFWyNlNg" target="_blank" rel="noopener noreferrer"  onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')" class="twitter" title="Youtube"><i class="bx bxl-youtube"></i></a></li>
          <li><a href="https://www.instagram.com/accounts/login/?next=/isro.dos/" target="_blank" rel="noopener noreferrer"  onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')" class="twitter" title="Instagram"><i class="bx bxl-instagram"></i></a></li>
          <li><a tabIndex="0" style="cursor:pointer;" onclick="increaseFontSize()" id="Ainc" title="Font size increase">A+&nbsp;</a></li>
          <li><a tabIndex="0" style="cursor:pointer;" onclick="resetFontSize()" id="Arest" title="Normal font size">A&nbsp;</a>  </li>      
          <li><a tabIndex="0" style="cursor:pointer;" onclick="decreaseFontSize ()" id="Adec" title="Font size decrease">A-&nbsp;</a></li>
          <li>  <a href="#main" title="Skip to main content"><span class="skiptomains">Skip to main content</span></a> </li>
        </ul>
      </div>
    </div>
   <!-- <div class="button-menu-mobile open-left" id="dotsID"><a href="#" onclick="mobileView()" > 
       <button title="more"><i class="bi bi-three-dots"></i></button>
     </a></div>  -->
    <div style="display: none;" class="topnavMob" id="myMob" >
      <p class="align-items-right" onclick="mobileViewClose()"><button type="button" class="btn-close btn-close-black" aria-label="Close"></button></p>
      <ul><li><a href="https://www.isro.gov.in/" class="English"  title="English" >English</a></li>
        <li><a href="https://www.isro.gov.in/ISRO_HINDI/" class="Hindi" title="Hindi">हिंदी</a></li>
        <li><a href="Sitemap.html" class="English" title="Sitemap" >Sitemap</a></li>
        <li><a href="contact.html" title="Contact Us">Contact us</a></li>
        <li><a href="https://www.isro.gov.in/ISROAPP/fFBF" target="_blank" rel="noopener noreferrer" title="Feedback">Feedback</a></li>
        <li><a href="RTI.html" title="RTI" >RTI</a></li>
        <li><a href="Careers.html" title="Career" >Career</a></li>
        <li><a href="Tenders.html"  title="Tender">Tender</a></li>
        <li><a href="FAQ.html" title="FAQ">FAQ</a></li>
        <li><a href="https://www.facebook.com/ISRO" target="_blank" rel="noopener noreferrer"  onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')"class="facebook" title="Facebook"><i class="bx bxl-facebook"></i></a>
          <a href="https://twitter.com/isro" target="_blank" rel="noopener noreferrer"  onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')" class="twitter bx" title="X"><svg xmlns="http://www.w3.org/2000/svg" width="10" height="13" fill="currentColor"  viewBox="0 3 16 16">
          <path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865l8.875 11.633Z"/>
        </svg></a><a href="https://www.youtube.com/channel/UCw5hEVOTfz_AfzsNFWyNlNg" target="_blank" rel="noopener noreferrer"   onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')"class="twitter" title="youtube"><i class="bx bxl-youtube"></i></a> <a href="https://www.instagram.com/accounts/login/?next=/isro.dos/" target="_blank" rel="noopener noreferrer"   onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')" class="twitter" title="instagram"><i class="bx bxl-instagram"></i></a></li>
         <li style="display:inline"> <a style="cursor:pointer;" onclick="increaseFontSize()" id="Ainc" title="A plus">A+&nbsp;</a>  <a style="cursor:pointer;" onclick="resetFontSize()" id="Arest" title="A">A&nbsp;</a> <a style="cursor:pointer;" onclick="decreaseFontSize ()" id="Adec" title="A minus">A-&nbsp;</a>  </li>  
         <li>    <a href="#main" title="Skip to main"><span class="skiptomain" style="color: #000000;">Skip to main </span></a> 
         </li>
        </ul>
      </div>
    </div>
  <header id="header" class="d-flex align-items-center">
    <div class="col-md-12">
    <div class="d-flex justify-content-between align-items-center BannerBg">
    <div class="container-fluid container-xl d-flex" style="position: relative;">               
    <a> <img loading="lazy"  class="bannerStyle" title="ISRO DOS Home" srcset="/media_isro/image/isromainBanner_NSPD25.png.webp 1024w,
    /media_isro/image/mob_banner_Nspd25.png.webp 640w,
    /media_isro/image/mob_banner_Nspd25.png.webp 320w" sizes="(max-width:640px) 100px, 100vw" src="/media_isro/image/isromainBanner_NSPD25.png.webp" alt="ISRO DOS Banner">
    <a href="https://www.isro.gov.in" target="_blank" rel="noopener noreferrer" title="ISRO DOS Home" style="position: absolute; left: 1%; width: 8%; top: 1%;  height: 100%;"></a>
    <a href="https://www.isro.gov.in/NSPD2025/" target="_blank" rel="noopener noreferrer" title="National Space Day - 2025" style="position: absolute; left: 80%; top: 1%; width: 8%; height: 100%;"></a>

<a href="https://www.india.gov.in" target="_blank" rel="noopener noreferrer" title="Government of India" onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')" style="position: absolute; left: 92%; top: 1%; width: 6%; height: 100%;"></a>
</a>
  


</div>
</div>
 <div class="page container-fluid container-xl d-flex align-items-center justify-content-lg-between">
      <!-- Uncomment below if you prefer to use an image logo -->
      <!-- <a href="index.html" class="logo me-auto me-lg-0"><img loading="lazy"   src="/media_isro/image/logo.png.webp" alt="" class="img-fluid"></a>-->
    <nav id="navbar" class="order-last order-lg-0 navbar" aria-label="isromenu">
       <ul class="navbar1 navbar2" id="menu" role="menubar" aria-label="isromenu" tabindex="0">
        <li role="none" id="limenu"><a role="menuitem" class="nav-link scrollto active" href="index.html" title="Home">Home</a></li>
        <li class="dropdown" role="none" id="limenu"><a role="menuitem" aria-haspopup="true" aria-expanded="false" href="#" title="About"><span>About</span> <i class="bi bi-chevron-down"></i></a>
        <ul role="menu" aria-label="About" class="secondLevel" id="secondLevel">
        <li role="none"><a role="menuitem" href="profile.html"  title="Profile">Profile</a></li>
        <li role="none"><a role="menuitem" href="Vision-Mission-Objectives.html" title="Vision-Mission-Objectives">Vision-Mission-Objectives</a></li>
        <li role="none"><a role="menuitem" href="citizencharter.html" title="Citizen charter">Citizen charter</a></li>
        <li role="none"><a role="menuitem" href="organisation.html" title="Organisational structure">Organisational structure </a></li>
        <li role="none"><a role="menuitem" href="isro_centre.html" title=" DoS Centers/units/enterprises"> DoS Centers/units/enterprises</a></li>
        <li role="none"><a role="menuitem" href="leadership.html" title="Secretary, DoS/ Chairman, ISRO">Secretary, DoS/ Chairman, ISRO</a></li>
        <li role="none"><a role="menuitem" href="formerchairman.html" title="Former Secretaries/Chairmen">Former Secretaries/Chairmen</a></li>
        <li role="none"><a role="menuitem" href="SpaceCommision.html" title="Space Commission"> Space Commission</a></li>
        <li role="none"><a role="menuitem" href="autonomous.html" title="Autonomous bodies">Autonomous bodies</a></li> 
        <li role="none"><a role="menuitem" href="genesis.html" title="Genesis">Genesis </a></li>
        <li role="none"><a role="menuitem" href="Timeline.html" title="Timeline">Timeline</a></li>                              
        <li role="none"><a role="menuitem" href="whoswho.html" title="Who's who">Who's who</a> </li>
        <li role="none"><a role="menuitem" href="contact.html" title="Contact us"> Contact us</a></li>
        </ul>
        </li>
        <li role="none" class="dropdown"><a role="menuitem" aria-haspopup="true" aria-expanded="false" href="#" title="Activities"><span> Activities</span> <i class="bi bi-chevron-down"></i></a>
        <ul role="menu" aria-label="Activities" class="secondLevel" id="secondLevel">
          <li role="none"><a role="menuitem" href="Mission.html" title="Missions accomplished">Missions accomplished</a></li>
          <li role="none"><a role="menuitem" href="FutureMissions.html" title="Upcoming Missions">Upcoming Missions</a></li>
          <li role="none"><a role="menuitem" href="Science.html" title="Science">Science</a></li>
          <li role="none"><a role="menuitem" href="Launchers.html" title="Launchers">Launchers</a></li>
          <li role="none"><a role="menuitem" href="Satellites.html" title="Satellites">Satellites</a></li>
          <li role="none"><a role="menuitem" href="SpaceApplications.html" title="Satellites">Space Applications</a></li>
          <li role="none"><a role="menuitem" href="researchdevelopment.html" title="Research & Development">Research & Development</a></li>
			  <li role="none"><a role="menuitem" href="Gaganyaan.html" title="Gaganyaan" >Gaganyaan</a></li>
			   <li role="none"><a role="menuitem" href="GroundSegmentActivities.html" title="Ground Segment activities">Ground Segment activities</a></li>
			    <li role="none"><a role="menuitem" href="IN-SPACe.html" title="Promotion & Authorisation">Promotion & Authorisation</a></li>
				<li role="none"><a role="menuitem" href="InternationalCoOperation.html" title="International co-operation">International co-operation</a></li>
        <li role="none"><a role="menuitem" href="CapacityBuilding.html" title="Capacity building">Capacity building</a></li>
        <li role="none"><a role="menuitem" href="Training.html" title="Training">Training</a></li>              
        <li role="none"><a role="menuitem" href="Outreach.html" title="Outreach">Outreach</a></li>                           
        </ul>
        </li>
    <li role="none" class="dropdown" ><a role="menuitem" aria-haspopup="true" aria-expanded="false" href="#" title="Services"><span>Services</span> <i class="bi bi-chevron-down"></i></a>
      <ul role="menu" aria-label="Services" class="secondLevel" id="secondLevel">
        <li role="none"><a role="menuitem" href="launchservices.html" title="Launch service">Launch service</a></li>
        <li role="none"><a role="menuitem" href="SatelliteSystemBusSubSystemTesting.html" title="Satellite: system, bus, sub-system, testing">Satellite: system, bus, sub-system, testing</a></li>
        <li role="none"><a role="menuitem" href="missionsupport.html"title="Mission support">Mission support</a></li>
        <li role="none"><a role="menuitem" href="GroundSystemSupport.html"  title="Ground systems support">Ground systems support</a></li>
        <li role="none"><a role="menuitem" href="SatelliteCommunicationApplications.html">Satellite Communication & Lease of transponders</a></li>
        <li role="none"><a role="menuitem" href="SpaceBasedEarthObservationServices.html"  title="Space based Earth observation: Bhuvan & Bhoonidhi">Space based Earth observation: Bhuvan & Bhoonidhi</a></li>
        <li role="none"><a role="menuitem" href="SatelliteNavigationServices.html" title="Satellite Navigation services">Satellite Navigation services</a></li>
        <li role="none"><a role="menuitem" href="MeteorologicalOceanographicApplications.html" title="Meteorological & Oceanographic Satellite Data">Meteorological & Oceanographic Satellite Data</a></li>             
        <li role="none"><a role="menuitem" href="DisasterManagementNationalInternational.html" title="Disaster Management: National & International">Disaster Management: National & International</a></li>             
        <li role="none"><a role="menuitem" href="AerialServicesDigitalMapping.html" title="Aerial Services & Digital Mapping">Aerial Services & Digital Mapping</a></li> 
        <li role="none"><a role="menuitem" href="North-EastIndiaRegionSpecificApplications.html" title="North-East India region specific applications Services">North-East India region specific applications Services</a></li>    
        <li role="none"><a role="menuitem" href="VedasServices.html" title="VEDAS services">VEDAS services</a></li>
        <li role="none"><a role="menuitem" href="TransferOrbitService.html" title="Transfer Orbit Service">Transfer Orbit Service</a></li>
				<li role="none"><a role="menuitem" href="SatelliteAidedSearchAndRescue.html" title="Satellite aided search & rescue">Satellite aided search & rescue</a></li>
      </ul>
    </li>
    <li role="none" class="dropdown" ><a role="menuitem" aria-haspopup="true" aria-expanded="false" href="#" title="Programmes"><span> Programmes</span> <i class="bi bi-chevron-down"></i></a>
    <ul role="menu" aria-label="Programmes" class="secondLevel" id="secondLevel">
      <li role="none"><a role="menuitem" href="AcademicCourses.html" title="Academic courses">Academic courses</a></li> 
      <li role="none"><a role="menuitem" href="Conference_Grants.html" title="Conference Grants">Conference Grants</a></li> 
      <li role="none"><a role="menuitem" href="Fellowships.html" title="Fellowships">Fellowships</a></li>
      <li role="none"><a role="menuitem" href="Merchandise.html" title="Space merchandise">Space merchandise</a></li>  
      <li role="none"><a role="menuitem" href="spacetutor.html" title="Space Tutor">Space Tutor</a></li> 
      <li role="none"><a role="menuitem" href="SpaceOnWheels.html" title="Space on wheels">Space on wheels</a></li>
      <li role="none"><a role="menuitem" href="Student_Program_Satellite.html" title="Student Satellite">Student Satellite</a></li>
      <li role="none"><a role="menuitem" href="TechnologyTransfer.html" title="Technology Transfer">Technology Transfer</a></li>
      <li role="none"><a role="menuitem" href="UNNATI.html" title="UNNATI">UNNATI</a></li>
      <li role="none"><a role="menuitem" href="YUVIKA.html" title="YUVIKA">YUVIKA</a></li>
    </ul>
    </li>       
    <li role="none" class="dropdown" ><a role="menuitem" aria-haspopup="true" aria-expanded="false" href="#" title="Resources"><span>Resources</span> <i class="bi bi-chevron-down"></i></a>
    <ul role="menu" aria-label="Resources" class="secondLevel" id="secondLevel">
      <li role="none"><a role="menuitem" href="River_Basin_Atlas.html" title=" Atlases: River basin "> Atlases: River basin</a></li>
      <li role="none"><a role="menuitem" href="https://bhuvan.nrsc.gov.in/" target="_blank" rel="noopener noreferrer"   onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')" title="Bhuvan">Bhuvan</a></li>
      <li role="none"><a role="menuitem" href="DBEM.html" title="Database for Emergency Management">Database for Emergency Management</a></li>
      <li role="none"><a role="menuitem" href="https://feast.vssc.gov.in/" target="_blank" rel="noopener noreferrer"   onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')" title="FEAST Tool">FEAST Tool</a></li>			 
      <li role="none"><a role="menuitem" href="https://igrasp.isro.gov.in/" target="_blank" rel="noopener noreferrer"   onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')" title=" I-grasp "> I-grasp</a></li>
      <li role="none"><a role="menuitem" href="InfoClimateEnv.html" title="Info for Climate & Enviroment studies">Info for Climate & Enviroment studies</a></li>
      <li role="none"><a role="menuitem" href="Landslide_Atlas_India.html" title="Landslide Atlas of India">Landslide Atlas of India</a></li>
      <li role="none"><a role="menuitem" href="https://www.mosdac.gov.in/live/index_one.php?url_name=india" target="_blank" rel="noopener noreferrer"   onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')" title="Meteorology & Oceanographic data">Meteorology & Oceanographic data</a></li>  
      <li role="none"><a role="menuitem" href="MobileApps.html">Mobile Apps</a></li>
      <li role="none"><a role="menuitem" href="MonthlySummary.html"  title="Monthly summary of DOS">Monthly Summary of DOS</a></li>
      <li role="none"><a role="menuitem" href="MOSDAC.html"  title="MOSDAC">MOSDAC</a></li>
      <li role="none"><a role="menuitem" href="https://www.sac.gov.in/Vyom/time_current" target="_blank" rel="noopener noreferrer"   onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')" title="NAVIC Time">NAVIC Time</a></li>
      <li role="none"><a role="menuitem" href="publications.html" title="Publications">Publications</a></li>  
        <li role="none"><a role="menuitem" href="https://bhuvan-app1.nrsc.gov.in/mhrd_ncert/" target="_blank" rel="noopener noreferrer" onclick="return confirm('You are visiting a link outside isro.gov.in. External Link that opens in a  new window.')" title="School Bhuvan - NCERT">School Bhuvan - NCERT</a></li>
      <li role="none"><a role="menuitem" href="Sciencedata.html" title="Science Data">Science Data</a></li>
      </ul>
      </li>
    <li role="none" class="dropdown" ><a role="menuitem" aria-haspopup="true" aria-expanded="false" href="#" title="Engagements">Engagements<i class="bi bi-chevron-down"></i></a>
    <ul role="menu" aria-label="EngageWithUS" class="secondLevel" id="secondLevel"> 
      
      <li role="none"><a role="menuitem" href="academia.html" title="Academia">Academia</a></li> 
      <li role="none"><a role="menuitem" href="https://www.isro.gov.in/ISROAPP/login.jsp" target="_blank" rel="noopener noreferrer" title="Ask an expert">Ask an expert</a></li>
      <li role="none"><a role="menuitem" href="Educators.html" title="Educators" > Educators </a></li>
      <li role="none"><a role="menuitem" href="Industry.html" title="Industry" title="Industry">Industry</a></li>
      <li role="none"><a role="menuitem" href="InternshipAndProjects.html" title="Internship & Projects">Internship & Projects</a></li> 
      <li role="none"><a role="menuitem" href="Careers.html" title="Join ISRO">Join ISRO</a></li>
      <li role="none"><a role="menuitem" href="Press.html" title="Media">Media</a></li>
      <li role="none"><a role="menuitem" href="Researchers_en.html" title="Researchers">Researchers</a></li>
      <li role="none"><a role="menuitem" href="Start_ups.html" title="Start_ups">Start-ups</a></li>
      <li role="none"><a role="menuitem" href="Students.html" title="Students">Students</a></li>
      <li role="none"><a role="menuitem" href="Training.html" title="Training">Training</a></li> 
      <li role="none"><a role="menuitem" href="Visitors.html" title="Visitors">Visitors</a></li> 
    </ul>
  </li>
  </ul>
  <i class="bi bi-list mobile-nav-toggle" id="mobileNavToggleISRO"></i>


<span id="searchidM" float="right"><input type="text" id="searchTextM" size="12" style="padding: 0 7px 0 7px !important; background: #fffff5d9; border: solid 0px rgb(255, 191, 0); font-size: 14px !important; margin-bottom: 0px !important;" placeholder="search" required>&nbsp;<img loading="lazy"  src="/media_isro/image/search-white.svg" onclick="searchTextM();" title="Search" style="cursor: pointer;"></span>
<div class="button-menu-mobile open-left" id="dotsID"><span onclick="mobileView()" style="padding: 2px;" > 
       <button title="more"><i class="fa" style="margin-left: 0px !important; font-size: 12px !important;">&#xf142</i></button>
     </span></div>
      </nav>
	  
	   <!-- <span><a href="search.html#gsc.q=lvm3"><img loading="lazy"  src="/media_isro/image/search.svg"></a></span> -->
<span id="searchidD" float="right"><input type="text" id="searchTextD" size="12" style="padding: 0 7px 0 7px !important; background: #fffff5d9; border: solid 0px rgb(255, 191, 0); font-size: 14px !important; margin-bottom: 0px !important;" placeholder="search" required>&nbsp;<img loading="lazy"  src="/media_isro/image/search-white.svg" onclick="searchTextD();" title="Search" style="cursor: pointer;"></span>




  
 <!--  <span id="searchidM" float="right">&nbsp;<img loading="lazy"  src="/media_isro/image/index/Ch3Logo.jpg" onclick="window.location.href= 'Chandrayaan3.html';" title="Chandrayaan3" style="cursor: pointer; width: 150px;background: #031d39;"></span>
  </nav>
  <span id="searchidD" float="right">&nbsp;<a href="Chandrayaan3.html"><img loading="lazy"  src="/media_isro/image/index/Ch3Logo.jpg" title="Chandrayaan3" style="cursor: pointer; width: 180px;background: #031d39;"></a></span>
-->

  <!-- .navbar -->     
  </div>
</div>
</header>`);

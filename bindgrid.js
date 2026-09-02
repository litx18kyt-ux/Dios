function BINDGRID(rowname, obj, bill_type) {
            $("#HDNBILL_TYPE").val(bill_type);
            //console.log($(obj).html());
            if (($(obj).html() != "" && $(obj).html() != "undefined" && $(obj).html() != undefined) || rowname == "valuewise") {
                // console.log($(obj).html());

                $("#btnBack").show();
                //var data_str = $("div#hidjsonHR").attr("data-hero");
                //var dataInit = JSON.parse(decodeURIComponent(data_str));
                var level = parseInt($("#hidHRlevel").attr("data-hero")) + 1;

                $("#hidHRlevel").attr("data-hero", level.toString())
                $("#MHRLEVELVAL").append("<option value='" + level.toString() + "' >" + $(obj).html() + "</option>");
                if ($("#ulhirarchy").children().length == 0) {
                    $("#ulhirarchy").append("<li style='float:left; padding:5px;' >" + $(obj).html() + "</li>");
                } else {
                    $("#ulhirarchy").append("<li  style='float:left; padding:5px;'  ><span class='k-icon k-i-arrow-60-right' ></span> " + $(obj).html() + "</li>");
                }
                console.log($("#MHRLEVEL option").eq(level).val() + " jeet");
                var data = [];
                if ($("#MHRLEVEL option").eq(level).val() == "BILL_PRINT") {

                    //return data= getbilldetails($(obj).html());

                    var posting_id_str = "";
                    var bill_doc_type = "";
                    setloader();
                    if (rowname == "valuewise") {
                        posting_id_str = obj;
                        bill_doc_type = bill_type
                    } else {
                        posting_id_str = $("#MBILL option[value='" + $(obj).html() + "']").text();
                    }

                    $.ajax({
                        url: 'PerformanceReview.aspx/getbilldetails',
                        type: "POST",
                        dataType: "json",
                        contentType: "application/json; charset=utf-8",
                        data: "{'POSTING_ID_STR':'" + posting_id_str + "','DOC_TYPE':'" + bill_doc_type + "'}",
                        async: false
                    }).done(function (data, status, xhr) {
                        removeloader();
                        var josondata = JSON.parse(data.d);
                        data = josondata.Table;
                        console.log(data);
                        BindGridData(data, level);

                    }).fail(function () {

                        removeloader();
                        debugger;
                        var grid = $("#grid").data("kendoGrid");
                        grid.hideColumn(grid.columns[1].columns[1]);
                    });

                    //data = datas;

                } else {
                    setloader();
                    ////////////////////////////////////
                    predicate = $(obj).html();
                    var prevcolname = $("#MHRLEVEL option").eq(level - 1).val();
                    var prevcolval = predicate;
                    var prevcolname1 = $("#MHRLEVEL option").eq(level - 1).val();
                    var prevcolval1 = predicate;
                    var prevcolname2 = $("#MHRLEVEL option").eq(level - 1).val();
                    var prevcolval2 = predicate;
                    if (level == 2) {
                        prevcolname = $("#MHRLEVEL option").eq(level - 2).val();
                        prevcolval = $('#MHRLEVELVAL option').eq($("#MHRLEVELVAL option").length - 2).text();
                    }
                    if (level == 3) {
                        prevcolname = $("#MHRLEVEL option").eq(level - 2).val();
                        prevcolval = $('#MHRLEVELVAL option').eq($("#MHRLEVELVAL option").length - 2).text();

                        prevcolname1 = $("#MHRLEVEL option").eq(level - 3).val();
                        prevcolval1 = $('#MHRLEVELVAL option').eq($("#MHRLEVELVAL option").length - 3).text();
                    }
                    if (level == 4) {
                        prevcolname = $("#MHRLEVEL option").eq(level - 2).val();
                        prevcolval = $('#MHRLEVELVAL option').eq($("#MHRLEVELVAL option").length - 2).text();

                        prevcolname1 = $("#MHRLEVEL option").eq(level - 3).val();
                        prevcolval1 = $('#MHRLEVELVAL option').eq($("#MHRLEVELVAL option").length - 3).text();

                        prevcolname2 = $("#MHRLEVEL option").eq(level - 4).val();
                        prevcolval2 = $('#MHRLEVELVAL option').eq($("#MHRLEVELVAL option").length - 4).text();
                    }

                    //var col_filter = prevcolname + "=\"" + prevcolval + "\" AND " + prevcolname1 + "='" + prevcolval1 + "' AND " + prevcolname2 + "='" + prevcolval2+"'"

                    //////////////////////////////////////

                    //data = (JSON.parse(filterHR(dataInit, $(obj).html(), level)));
                    $.ajax({
                        url: 'PerformanceReview.aspx/GETGROUPEDBYDATAGRID',
                        type: "POST",
                        contentType: "application/json; charset=utf-8",
                        dataType: "json",
                        data: "{ 'GROUPCOLUMN': '" + $("#MHRLEVEL option").eq(level).val() + "', 'FILTERCOLUMN': '" + $("#MHRLEVEL option").eq(level).val() + "', 'FILTERCOLUMN1': '" + prevcolname + "', 'FILTERCOLUMN2': '" + prevcolname1 + "', 'FILTERCOLUMN3': '" + prevcolname2 + "', 'FILTERCOLUMN_VALUE1': '" + prevcolval + "', 'FILTERCOLUMN_VALUE2': '" + prevcolval1 + "', 'FILTERCOLUMN_VALUE3': '" + prevcolval2 + "' }",
                        //timeout: 600000
                        async: true,
                        cache: false,
                    }).done(function (data, status, xhr) {
                        removeloader();
                        var josondata = JSON.parse(data.d);
                        console.log(josondata);
                        var data = josondata.Table;
                        BindGridData(data, level);
                    });

                }

                //console.log(data);

            } else {
                $("#MHRLEVELVAL").children().remove();
                $("#ulhirarchy").children().remove();
                $("#hidHRlevel").attr("data-hero", "0");
                $("#btnBack").hide();
                var LOGIN_PA_ID = 0;
                var PA_ID = 0;
                var HQ_ID = '1';
                var FMONTH = "";
                var TMONTH = ""
                var COLUMN = (rowname == "" ? "PRI_VAL,SEC_VAL,TGT_VAL" : rowname);
                var WISE = ""
                var WISE1 = ""
                var ROW_GROUP_ON = 2
                var MAIN_GROUP_ON = 0
                var WISEFILTER = '0';
                var GROUPFILTER = '0';
                var LRTYPE = "R";
                var QVTYPE = "V";
                var SPL_ID = 0;
                var STATE_ID = 0;
                var HQ_ID = 0;
                var ITEM_ID = 0;
                var ITEMG_ID = 0;
                var STK_ID = 0;
                var COMPANY_ID = 0;
                var STK_STATUS_P = 0;
                var STK_STATUS_S = 0;
                var CRM_HQ_GROUP_ID = 0;
                //------------------------ VARIABLE INTIALIZATION ---------------------------------------------------------
                //debugger;
                LOGIN_PA_ID = $("#MPA_ID").val();  //"<%=Session("PA_ID")%>";
                PA_ID = $("#HIDLOGINID", window.parent.document).val();
                FMONTH = $("#MFDATE").val();
                TMONTH = $("#MTDATE").val();
                var DATEYN = 0;
                if ($("#chkDateWise").is(":checked")) {
                    if ($("#EFDATE").val() == "") {
                        alert("Please enter from date");
                        removeloader();
                        openoptionmodal();
                        return false;
                    }
                    if ($("#ETDATE").val() == "") {
                        alert("Please enter to date");
                        removeloader();
                        openoptionmodal();
                        return false;
                    }
                    if ($("#EFDATE").val() != "") {
                        FMONTH = $("#EFDATE").val().split("/")[1] + "/" + $("#EFDATE").val().split("/")[0] + "/" + $("#EFDATE").val().split("/")[2];
                    }
                    if ($("#ETDATE").val() != "") {
                        TMONTH = $("#ETDATE").val().split("/")[1] + "/" + $("#ETDATE").val().split("/")[0] + "/" + $("#ETDATE").val().split("/")[2];
                    }
                    DATEYN = 1;
                }
                console.log(FMONTH);
                console.log(TMONTH);
                //////////////////////////////
                var MonthFIndex = $("#MFDATE").children().length - 1;
                var MonthFVal = $("#MFDATE option").eq(MonthFIndex).val();
                var MonthLIndex = $("#MTDATE").children().length - 2;
                var MonthLVal = $("#MTDATE option").eq(MonthLIndex).val();
                if ($("#MCUMULATIVE").val() == "1") {
                    //FMONTH = MonthFVal;
                    //TMONTH = MonthLVal;
                }
                /////////////////////////////
                //COLUMN = "PRI_VAL,SEC_VAL,TGT_VAL,ACH"
                var index = $("#MDDLSUMMARY").children().length - 2;
                var lastval = $("#MDDLSUMMARY option").eq(index).val();
                var index1 = $("#MDDLSUMMARY").children().length - 3;
                var lastval1 = $("#MDDLSUMMARY option").eq(index1).val();

                WISE = $("#MDDLSUMMARY").val();
                console.log(WISE);

                ROW_GROUP_ON = $("#MGROUPING_ID").val();

                if ($("#MGROUPING_ID").val() == "0" && COLUMN.toString().indexOf("ADJ") == "-1") {
                    ROW_GROUP_ON = $("#MDDLSUMMARY").val();
                }
                var GROUP_COULUMN = "";
                //if ($("#MGROUPING_ID").val() == "P")
                //{
                //    GROUP_COULUMN = $("#MGROUPING_ID_HDN option[value='" + $("#MGROUPING_ID").val() + "']").text() + "," + $("#MGROUPING_ID_HDN option[value='" + $("#MDDLSUMMARY").val() + "']").text();
                //    WISE = "GD";
                //}
                //else {
                if ($("#MDDLSUMMARY option:selected").index() > ($("#MGROUPING_ID option:selected").index() - 1) && $("#MGROUPING_ID option:selected").index() > 0) {

                    //ROW_GROUP_ON = $("#MDDLSUMMARY").val();
                    //WISE = $("#MGROUPING_ID").val();
                    GROUP_COULUMN = $("#MGROUPING_ID_HDN option[value='" + $("#MGROUPING_ID").val() + "']").text() + "," + $("#MGROUPING_ID_HDN option[value='" + $("#MDDLSUMMARY").val() + "']").text();
                    WISE = "GD";

                }
                //}
                if (WISE == "null" || WISE == undefined || WISE == "undefined") {
                    if (window.parent.loadPageVar("COL") != "") {
                        WISE = window.parent.loadPageVar("COL");
                    }
                }
                if (ROW_GROUP_ON == "null" || ROW_GROUP_ON == undefined || ROW_GROUP_ON == "undefined") {
                    if (window.parent.loadPageVar("COL") != "") {
                        ROW_GROUP_ON = window.parent.loadPageVar("COL");
                    }
                }
                GROUPFILTER = "0"
                //$("#MGFRILTER").val();
                WISEFILTER = "0"
                //$("#MGF").val();
                LRTYPE = $("#MRLTYPE").val();
                TARGET_ID = $("#MVALUETYPE").val();


                var vMDIVISION_ID = $("#MDIVISION_ID").val();
                var itemStr = "0";
                if ($("#MDIVISION_ID").val() != null) {
                    for (i = 0; i < vMDIVISION_ID.length; i++) {
                        if (itemStr == "") {
                            itemStr = vMDIVISION_ID[i];
                        } else {
                            itemStr = itemStr + "," + vMDIVISION_ID[i];
                        }
                    }
                }
                SPL_ID = itemStr;

                CRM_HQ_GROUP_ID = $("#MCRM_HQ_GROUP_ID").val();
                if (CRM_HQ_GROUP_ID == null || CRM_HQ_GROUP_ID == undefined || CRM_HQ_GROUP_ID == "undefined") {
                    CRM_HQ_GROUP_ID = "0";
                }

                HQ_ID = $("#MHQ_ID").val();
                if (HQ_ID == null || HQ_ID == undefined || HQ_ID == "undefined") {
                    HQ_ID = "0";
                }
                STATE_ID = $("#MSTATE_ID").val();
                if (STATE_ID == null || STATE_ID == undefined || STATE_ID == "undefined") {
                    STATE_ID = "0";
                }
                //ITEM_ID = $("#MITEM_ID").val();

                var Items = $("#MITEM_ID").val();
                //console.log($("#MITEM_ID").val());
                var itemStr = "0";
                if ($("#MITEM_ID").val() != null) {
                    for (i = 0; i < Items.length; i++) {
                        if (itemStr == "") {
                            itemStr = Items[i];
                        } else {
                            itemStr = itemStr + "," + Items[i];
                        }

                    }
                }
                ITEM_ID = itemStr;

                var vMITEMG_ID = $("#MITEMG_ID").val();
                var itemStr = "0";
                if ($("#MITEMG_ID").val() != null) {
                    for (i = 0; i < vMITEMG_ID.length; i++) {
                        if (itemStr == "") {
                            itemStr = vMITEMG_ID[i];
                        } else {
                            itemStr = itemStr + "," + vMITEMG_ID[i];
                        }
                    }
                }
                ITEMG_ID = itemStr;

                if ($("#HIDCOMPANY", window.parent.document).val() == "STEAD" && window.parent.loadPageVar("COL") == "TGT_VAL_GRP" && ITEMG_ID == "0") {
                    ITEMG_ID = "4100";
                }

                var ITEM_HR = "";
                var ITEM_HR_ZERO = "";
                var BILLYN = "";
                if ($("#chkHRITEM").is(":checked") == true || $("#MGROUPING_ID").val() == 'P' || $("#MDDLSUMMARY").val() == 'P') {
                    ITEM_HR = "1";

                } else {
                    ITEM_HR = "0";
                    $("#chkHRITEM").prop("checked", "")
                }
                if ($("#chkHRITEMZERO").is(":checked") == true) {
                    ITEM_HR_ZERO = "1";
                    ITEM_HR = "1";

                } else {
                    ITEM_HR_ZERO = "0";
                }
                if ($("#chkBILLLEVEL").is(":checked") == true) {
                    BILLYN = "1";
                } else {
                    BILLYN = "0";
                }

                var rounddata = "";
                if ($("#DECPLACE").val() == "0") {

                    rounddata = "1";

                } else {
                    rounddata = "0";
                }

                ///////// stockist DDL -------------------------------
                var DDLSTK_ID = $("#DDL_STOCKIST").val();
                var STK_IDSTR = "0";
                if ($("#DDL_STOCKIST").val() != null) {
                    for (i = 0; i < DDLSTK_ID.length; i++) {
                        if (STK_IDSTR == "") {
                            STK_IDSTR = DDLSTK_ID[i];
                        } else {
                            STK_IDSTR = STK_IDSTR + "," + DDLSTK_ID[i];
                        }

                    }
                }

                ///////// CONSIGNEE DDL -------------------------------
                var DDLCNF_ID = $("#DDL_CONSIGNEE").val();
                var CNF_IDSTR = "0";
                if ($("#DDL_CONSIGNEE").val() != null) {
                    for (i = 0; i < DDLCNF_ID.length; i++) {
                        if (CNF_IDSTR == "") {
                            CNF_IDSTR = DDLCNF_ID[i];
                        } else {
                            CNF_IDSTR = CNF_IDSTR + "," + DDLCNF_ID[i];
                        }

                    }
                }

                COMPANY_ID = CNF_IDSTR;
                var vMonth_QTR = 0;
                if ($("#MCUMULATIVE").val() == "3" || $("#MCUMULATIVE").val() == "2") {
                    vMonth_QTR = 1;
                }
                var HORIZONTALYN = 0;
                if ($("#MORIENT").val() == "1") {
                    HORIZONTALYN = 1;
                }

                //debugger
                STK_ID = STK_IDSTR;
                STK_STATUS_P = $("#MSTATUS_P").val();
                STK_STATUS_S = $("#MSTATUS_S").val();
                var iLYSALE_ON_CYTEAM = 0;
                if ($("#chksalenetworkyn").is(":checked") == true) {
                    iLYSALE_ON_CYTEAM = 1;
                }
                var iOUTST_PERIOD = 0;
                if ($("#chkOutstperiod").is(":checked") == true) {
                    iOUTST_PERIOD = 1;
                }

                var iOUTST_BALANCE = 0;
                if ($("#chkOUTSTBALANCE").is(":checked") == true) {
                    iOUTST_BALANCE = 1;
                }

                var sADD_COL = ""
                var ADD_COL = $("#MADDCOL").val();
                if ($("#MADDCOL").val() != null) {
                    for (i = 0; i < ADD_COL.length; i++) {
                        console.log(ADD_COL[i]);
                        if (ADD_COL[i] != "0") {
                            if (sADD_COL == "") {
                                sADD_COL = ADD_COL[i];
                            } else {
                                sADD_COL = sADD_COL + "," + ADD_COL[i];
                            }
                        }
                    }
                }
                var vPRI_PERIOD = 0
                if ($("#CHKPRIPERIOD").is(":checked") == true) {
                    vPRI_PERIOD = "1";

                }



                // STK_ID=  $("#DDL_STOCKIST").val();
                //--------------------------------------------------------

                var rounddata = "";
                if ($("#DECPLACE").val() == "0") {

                    rounddata = "1";

                } else {
                    rounddata = "0";
                }
                //////////////////////////////////////////////////////
                debugger;
                var vMITEMG_ID_2 = $("#MITEMG_ID_2").val();
                var itemStr_2 = "0";
                if ($("#MITEMG_ID_2").val() != null) {
                    for (i = 0; i < vMITEMG_ID_2.length; i++) {
                        if (itemStr_2 == "") {
                            itemStr_2 = vMITEMG_ID_2[i];
                        } else {
                            itemStr_2 = itemStr_2 + "," + vMITEMG_ID_2[i];
                        }
                    }
                }
                var ITEMG_ID_2 = itemStr_2;

                /////////////////////////////////////////////
                var vMITEMG_ID_3 = $("#MITEMG_ID_3").val();
                var itemStr_3 = "0";
                if ($("#MITEMG_ID_3").val() != null) {
                    for (i = 0; i < vMITEMG_ID_3.length; i++) {
                        if (itemStr_3 == "") {
                            itemStr_3 = vMITEMG_ID_3[i];
                        } else {
                            itemStr_3 = itemStr_3 + "," + vMITEMG_ID_3[i];
                        }
                    }
                }

                var ITEMG_ID_3 = itemStr_3;

                var vMITEMG_ID_4 = $("#MITEMG_ID_4").val();
                var itemStr_4 = "0";
                if ($("#MITEMG_ID_4").val() != null) {
                    for (i = 0; i < vMITEMG_ID_4.length; i++) {
                        if (itemStr_4 == "") {
                            itemStr_4 = vMITEMG_ID_4[i];
                        } else {
                            itemStr_4 = itemStr_4 + "," + vMITEMG_ID_4[i];
                        }
                    }
                }

                var ITEMG_ID_4 = itemStr_4;

                var PartyGroup_Str = "0";
                if ($("#HIDCOMPANY", window.parent.document).val() == "ICON") {
                    PartyGroup_Str = $("#MPartyGroup").val();
                }
                else {
                    var vMPARTY_GROUP = $("#MParty_Group").val();
                    if ($("#MParty_Group").val() != null) {
                        for (i = 0; i < vMPARTY_GROUP.length; i++) {
                            if (PartyGroup_Str == "") {
                                PartyGroup_Str = vMPARTY_GROUP[i];
                            } else {
                                PartyGroup_Str = PartyGroup_Str + "," + vMPARTY_GROUP[i];
                            }
                        }
                    }
                }

                var PARTY_GROUP = PartyGroup_Str;



                //if (ITEMG_ID != "0" && ITEMG_ID_2 != "0" && ITEMG_ID_3 != "0")
                //{

                //}
                //else {
                //    if (ITEMG_ID != "0" || ITEMG_ID_2 != "0" || ITEMG_ID_3 != "0") {
                //        ITEMG_ID = ITEMG_ID + "," + ITEMG_ID_2 + "," + ITEMG_ID_3
                //        ITEMG_ID_2 = ITEMG_ID + "," + ITEMG_ID_2 + "," + ITEMG_ID_3
                //        ITEMG_ID_3 = ITEMG_ID + "," + ITEMG_ID_2 + "," + ITEMG_ID_3
                //    }
                //}
                //, SPL_ID, STATE_ID, HQ_ID, ITEM_ID, ITEMG_ID
                var MITEM_STATUS = $("#MITEM_STATUS").val();
                var SALE_SHARE = $("#MSALE_SHARE").val();
                $("#grid").html('');
                $('#grid').css("height", "400px");
                $.ajax({
                    url: 'PerformanceReview.aspx/GETDATAGRID',
                    type: "POST",
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    data: "{ 'LOGIN_PA_ID': '" + LOGIN_PA_ID + "', 'GROUPON': '" + ROW_GROUP_ON + "', 'WISE': '" + WISE + "', 'FMONTH': '" + FMONTH + "', 'TMONTH': '" + TMONTH + "', 'COLUMN': '" + COLUMN + "','DATEYN':'" + DATEYN + "','GROUPFILTER':'" + GROUPFILTER + "', 'WISEFILTER':'" + WISEFILTER + "' , 'TARGET_ID':'" + TARGET_ID + "' , 'LRTYPE':'" + LRTYPE + "',  'SPL_ID':'" + SPL_ID + "',  'STATE_ID':'" + STATE_ID + "',  'HQ_ID':'" + HQ_ID + "',  'ITEM_ID':'" + ITEM_ID + "',  'ITEMG_ID':'" + ITEMG_ID + "','ITEM_HR':'" + ITEM_HR + "','GROUP_COULUMN':'" + GROUP_COULUMN + "','STK_ID':'" + STK_ID + "',ITEM_STATUS:'" + MITEM_STATUS + "',QTRWISE_TOTALYN:'" + vMonth_QTR + "',HORIZONTALYN:'" + HORIZONTALYN + "',BILLYN:'" + BILLYN + "','ITEM_HR_ZERO':'" + ITEM_HR_ZERO + "','STK_STATUS_P':'" + STK_STATUS_P + "' ,'STK_STATUS_S':'" + STK_STATUS_S + "',SALE_SHARE:'" + SALE_SHARE + "',iLYSALE_ON_CYTEAM:'" + iLYSALE_ON_CYTEAM + "',sADD_COL:'" + sADD_COL + "' ,iPRI_PERIOD:'" + vPRI_PERIOD + "',iROUDATA:'" + rounddata + "', iOUTST_PERIOD:'" + iOUTST_PERIOD + "', ITEMG_ID_2:'" + ITEMG_ID_2 + "', ITEMG_ID_3:'" + ITEMG_ID_3 + "', iOUTST_BALANCE:'" + iOUTST_BALANCE + "','COMPANY_ID':'" + COMPANY_ID + "','CRM_HQ_GROUP_ID':'" + CRM_HQ_GROUP_ID + "', ITEMG_ID_4:'" + ITEMG_ID_4 + "', PARTY_GROUP:'" + PARTY_GROUP + "' }",//ITEMG_ID_2
                    //timeout: 600000
                    async: true,
                    cache: false,
                }).done(function (data, status, xhr) {
                    //console.log(data.d.length);
                    if (data.d.length <= 2) {
                        removeloader();
                        return false;
                    }
                    //console.log(data.d);
                    var data_str1 = encodeURIComponent(JSON.stringify(JSON.parse(data.d).Table));
                    var data_str2 = encodeURIComponent(JSON.stringify(JSON.parse(data.d).Table2));
                    var josondata = JSON.parse(data.d);
                    console.log(josondata);
                    var data = josondata.Table;
                    var data1 = josondata.Table1;
                    var data2 = josondata.Table2;
                    var data3 = josondata.Table3;
                    var data4 = josondata.Table4;
                    var data5 = josondata.Table5;
                    var data6 = josondata.Table6;
                    _data5 = data5;

                    //$("div#hidjson").attr("data-hero", data_str);
                    //$("div#hidjsonHR").attr("data-hero", data_str1);

                    $("div#hidjsonRetioPercent").attr("data-hero", data_str2);

                    $("#MHRLEVEL").children().remove();
                    $("#MREP_COL").val("");
                    $("#MREP_COL2").val("");
                    $("#GROUP_COL3").val("");
                    $("#GROUP_COL4").val("");
                    if (data1.length > 0) {
                        if (data1[0]["REPL_COL"].length > 0) {
                            $("#MREP_COL").val(data1[0]["REPL_COL"]);
                        }
                        if (data1[0]["REPL_COL_TO"].length > 0) {
                            $("#MREP_COL2").val(data1[0]["REPL_COL_TO"]);
                        }
                        if (data1[0]["GROUP_COLUMN_CNT"].length > 0) {
                            $("#GROUP_COL3").val(data1[0]["GROUP_COLUMN_CNT"]);
                            $("#GROUP_COL4").val(data1[0]["GROUP_COLUMN_CNT_TYPE"]);
                        }

                    }
                    if (data3.length > 0) {
                        $("#MBILL").children().remove();
                        for (i = 0; i < data3.length; i++) {
                            $("#MBILL").append("<option value='" + data3[i]["STK_NAME"] + "' >" + data3[i]["POSTING_ID"] + "</option>");
                        }
                    }
                    if (data4.length > 0) {
                        $("#MBILL1").children().remove();
                        for (i = 0; i < data4.length; i++) {
                            if (data4[i]["STK_NAME"] != "") {
                                $("#MBILL1").append("<option value='" + data4[i]["STK_NAME"] + "_" + data4[i]["DOC_TYPE"] + "' >" + data4[i]["POSTING_ID"] + "</option>");
                            }
                        }
                    }
                    if (data5.length > 0) {
                        $("#MCOLAVG").children().remove();
                        $("#MHIDE_COL").children().remove();
                        for (i = 0; i < data5.length; i++) {
                            if (data5[i]["HIDE_COL"] == "Y") {
                                $("#MHIDE_COL").append("<option value='" + data5[i]["COLM_NAME"] + "' >" + data5[i]["COLM_CAP"] + "</option>");
                            }
                            $("#MCOLAVG").append("<option value='" + data5[i]["COLM_NAME"] + "' >" + data5[i]["COLM_CAP"] + "</option>");
                        }
                    }
                    if (data6.length > 0) {
                        $("#MCOL_TABLE6").children().remove();

                        for (i = 0; i < data6.length; i++) {
                            if (data6[i]["PERCENT_COL"] != "") {
                                $("#MCOL_TABLE6").append("<option value='" + data6[i]["PERCENT_COL"] + "' >" + data6[i]["TARGET_COL"] + "," + data6[i]["VALUE_COL"] + "</option>");
                            }
                        }
                    }

                    $("#DOC_TYPE").val("");
                    $("#PERCENT_COL").val("");
                    $("#TARGET_COL").val("");
                    $("#VALUE_COL").val("");

                    if (data2.length > 0) {

                        if (data2[0]["DOC_TYPE"].length > 0) {
                            $("#DOC_TYPE").val(data2[0]["DOC_TYPE"]);
                        }

                        if (data2[0]["PERCENT_COL"].length > 0) {
                            $("#PERCENT_COL").val(data2[0]["PERCENT_COL"]);
                        }

                        if (data2[0]["TARGET_COL"].length > 0) {
                            $("#TARGET_COL").val(data2[0]["TARGET_COL"]);
                        }

                        if (data2[0]["VALUE_COL"].length > 0) {
                            $("#VALUE_COL").val(data2[0]["VALUE_COL"]);
                        }
                        //if (data2[0]["HIDE_COL"].length > 0) {
                        //    $("#HIDE_COL").val(data2[0]["HIDE_COL"]);
                        //}
                        for (i = 0; i < data2.length; i++) {
                            if (i != 0) {
                                if (data2[0]["DOC_TYPE"].length > 0) {
                                    $("#DOC_TYPE").val($("#DOC_TYPE").val() + "," + data2[i]["DOC_TYPE"]);
                                }

                                if (data2[0]["PERCENT_COL"].length > 0) {
                                    $("#PERCENT_COL").val($("#PERCENT_COL").val() + "," + data2[i]["PERCENT_COL"]);
                                }

                                if (data2[0]["TARGET_COL"].length > 0) {
                                    $("#TARGET_COL").val($("#TARGET_COL").val() + "," + data2[i]["TARGET_COL"]);
                                }

                                if (data2[0]["VALUE_COL"].length > 0) {
                                    $("#VALUE_COL").val($("#VALUE_COL").val() + "," + data2[i]["VALUE_COL"]);
                                }
                            }
                        }

                    }
                    if ($("#MDDLSUMMARY").val() == "RD") {
                        removeloader();
                        $("#grid").html("");
                        window.location.href = 'OpenExcel.aspx?title=' + $("#reportheader").text();
                        //var data_str = $("div#hidjson").attr("data-hero");
                        //var data_str = $("div#hidjsonHR").attr("data-hero");
                        //var my_object = JSON.parse(decodeURIComponent(data_str));
                        //exportExcel(my_object);
                    }
                    else {
                        debugger;
                        BindGridData(data, "0");
                    }


                    //for (i = 0; i < data5.length; i++) {
                    //    if (data5[i]["HIDE_COL"] == "Y") {

                    //        for (var j = 0; j < length; j++) {



                    //        }
                    //    }
                    //}

                    //$("#grid").find("table th").eq(1).hide();




                    $contentLoadTriggered = false;
                })
                    .fail(function () {
                        removeloader();

                    });



            }

        }
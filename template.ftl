[<#list reports as report>
    <#-- Report level -->
    <#list report.transactionList as expense>
    {   "reportID"                      :    "${expense.reportID}",
        "accountID"                     :    "${report.accountID}",
        "accountEmail"                  :    "${report.accountEmail}",
        "employeeid"                    :    "${report.employeeCustomField1 }",
        "created"                       :    "${expense.created}",
        <#if expense.modifiedCreated?has_content>
        "created"                       :    "${expense.modifiedCreated}"
        <#else>
        "created"                       :    "${expense.created}"
        </#if>,
        "tag"                           :    "${expense.tag}",
        "convertedAmount"               :    "${expense.convertedAmount/100}",
        "currencyConversionRate"        :    "${expense.currencyConversionRate}",
        "currency"                      :    "${expense.currency}",
        "merchant"                      :    "${expense.merchant}",
        "category"                      :    "${expense.category?j_string}",
        <#if expense.modifiedAmount?has_content>
        "modifiedAmount"                :    "${expense.modifiedAmount/100}"
        <#else>
        "modifiedAmount"                :    "${expense.amount/100}"
        </#if>
    }<#if expense?has_next>,<#else><#if report?has_next>,</#if></#if>
    </#list>
</#list>
]

# Alignment audit - suite 30279

- Cases audited: **190**
- Blocking findings: **0**
- Advisory (reviewed-intentional) findings: **196**

## Residual mojibake in any field - 0
_none_

## Title missing the ' - ' feature separator _(advisory)_ - 181
- C4102757 | Same-fare correction holds the Metro cap
- C4102758 | Correction outside the Metro zone removes the cap and charges the difference
- C4102759 | Correction into the Metro zone applies the cap and refunds the difference
- C4102760 | Correcting a settled free (capped) tap keeps it at £0.00
- C4102761 | Correcting a settled partially-capped tap keeps it at £1.70
- C4102762 | A correction never pushes the day total over the Metro cap
- C4102763 | A corrected capped tap stays settled and free
- C4102764 | Correcting the first full-fare tap leaves its charge unchanged
- C4102765 | Correcting an unsettled capped tap re-evaluates and stays free
- C4102766 | A declined journey is not treated as a settled capped tap
- C4102767 | Re-running settlement after a correction does not re-charge the capped tap
- C4102768 | Higher-fare correction within the zone holds the cap
- C4102769 | Higher-fare correction outside the zone removes the cap and charges the difference
- C4102770 | Lower-fare correction within the zone keeps the day above cap and holds
- C4102771 | Lower-fare correction drops the day below cap and refunds
- C4102772 | Zone 4 correction within the highest band holds the cap
- C4102773 | Correction into a capped zone audits a free tap under the zonal cap
- C4102774 | A correction into a capped zone does not increase the account total
- C4102775 | The cap shown after a correction is the zonal cap, not a reference cap
- C4102776 | Correcting into a zone below cap charges toward the zonal cap
- C4102777 | A journey with no zonal cap still uses the reference cap correctly
- C4102778 | Correcting to another stop in the same zone keeps the zonal cap
- C4102779 | Re-running settlement after a zonal correction adds no charge
- C4102780 | The zonal cap applies after a correction regardless of transport mode
- C4102781 | Correction to a higher ref removes the cap and charges the difference
- C4102782 | Correction to a lower ref below the cap removes it and refunds
- C4102783 | Correction to a lower ref still above the cap charges the extra
- C4102784 | Single uncapped tap raised to a higher fare charges the difference
- C4102785 | Single uncapped tap lowered refunds the difference
- C4102786 | Aligning two different-ref taps to the same ref applies the cap and refunds
- C4102787 | Lowering the higher-ref tap to match applies the lower cap and refunds
- C4102788 | Correction within the town service zone holds the cap
- C4102789 | Correction outside the town to a higher fare removes the cap and charges the difference
- C4102790 | Correction outside the town to a lower fare removes the cap and refunds
- C4102791 | Re-tap at the same stage after annulment is the first good tap (Metro)
- C4102792 | Full Metro day reaches the daily cap after an annulment
- C4102793 | Re-tap at the same stage after annulment is the first ref fare tap (Ulsterbus)
- C4102794 | Ulsterbus reference fare cap applies on the correct tap after annulment
- C4102795 | Re-tap after annulment in the ref.61 band caps at the ref.61 value
- C4102796 | Annulment in the ref.60 band does not borrow the higher ref.61 cap
- C4102797 | Genuine duplicate without annulment is still rejected as £0.00
- C4102798 | Re-tap at a different stage after annulment is a normal first tap
- C4102799 | Annulling the re-tap as well leaves a later tap as the first good tap
- C4102800 | Annulment processed in the same settlement run as the re-tap
- C4102801 | Annulment with no re-tap leaves no chargeable journey
- C4102802 | Annulling a capped tap does not corrupt the day total
- C4102803 | Annulling the first capped-day tap then re-tapping restores correct totals
- C4102804 | Annulment on one card does not affect a similar tap on another card
- C4102805 | Ulsterbus re-tap with a different alighting and fare after annulment
- C4102806 | Re-tap at the same stage without an annulment is a genuine duplicate
- C4102807 | Multiple annulment and re-tap cycles in one day cap correctly
- C4102808 | Annulment on a previous day does not affect the new day's first tap
- C4102809 | A valid tap rejected as duplicate is retained when the first tap is cancelled
- C4102810 | Several same-stage taps then cancelling the first promotes the next valid tap
- C4102811 | No valid journey is left missing after the annulment
- C4102812 | Annulment processed before the second tap makes it a normal first journey
- C4102813 | Cancelling the rehabilitated tap promotes the next tap in turn
- C4102814 | Cancelling a tap with no following tap leaves nothing missing
- C4102815 | A second tap from a different stage is unaffected by the annulment
- C4102816 | Second tap after a same-stage retail transaction is flagged duplicate
- C4102817 | Later taps including an out-of-order timestamp are flagged duplicates
- C4102818 | Multiple interleaved retail transactions never reset the duplicate reference
- C4102819 | A retail transaction from a different stage still allows the duplicate
- C4102820 | A same-stage tap outside the duplicate window is not a duplicate
- C4102821 | The retail transaction itself is never flagged a duplicate of a tap
- C4102822 | A later tap from a different boarding stage is a genuine new tap
- C4102823 | A cancelled journey remains visible in Journey History
- C4102824 | A cancelled journey with a £0.00 fare is still visible
- C4102825 | Editing the alighting stop on a cancelled tap keeps the journey visible
- C4102826 | A zero-fare correction on a cancelled tap leaves a single visible row
- C4102827 | Editing the stop on a non-cancelled journey still works
- C4102828 | A cancelled journey stays cancelled after a stop correction and further settlement
- C4102829 | Cancelling one journey does not affect other visible journeys
- C4102830 | Cancelling a charged journey produces a refund and retains the record
- C4102831 | Editing the stop on a cancelled tap after settlement keeps the record
- C4102832 | A cancelled transfer journey remains visible
- C4102833 | A settled TOO journey shows its onward stops, not "No options"
- C4102834 | A settled TOO journey from another stage shows its onward stops
- C4102835 | Both settled ref.60 taps from the same stage populate the dropdown
- C4102836 | Re-opening the Update Stop modal always populates the dropdown
- C4102837 | "No options" is correct when the boarding stage is the last stop
- C4102838 | The correct operator returns stops; a mismatched operator returns none
- C4102839 | Only stops with a fare greater than zero are shown
- C4102840 | Zero-fare transfer stops are not shown
- C4102841 | Valid stops with a positive fare are still shown
- C4102842 | Selecting a valid positive-fare stop updates the journey
- C4102843 | A zero-fare stop is hidden but the smallest positive-fare stop is shown
- C4102844 | A £0.00 capped journey stays visible and editable
- C4102845 | A cancelled £0.00 journey stays visible and editable
- C4102846 | A transfer journey charged £0.00 stays displayed
- C4102847 | A stop with a negative fare is not shown
- C4102848 | Transfer stops with a positive fare still appear
- C4102849 | TVM-only stops with a positive fare still appear
- C4102850 | A recoverable debt is recovered and the card returns to Active
- C4102851 | An unrecoverable debt leaves the cards Blocked
- C4102852 | Visa MIT recovery clears a recoverable issuer-liability debt
- C4102853 | A successful recovery removes the card from the Deny List
- C4102854 | The recovered account is visible in the Operator Portal with the correct status
- C4102855 | Recovery behaviour is observable in the Operator Portal, logging verified by dev tests
- C4102945 | A card is added to the Deny List when it fails payment authorisation
- C4102946 | A card on the Deny List is prevented from future travel until resolved
- C4102947 | A card is removed from the Deny List when its debt is recovered
- C4102856 | Operator sign-on and navigation
- C4102857 | Access rights differ by user role
- C4102858 | Operator can log out
- C4102859 | Search and filter customers
- C4102860 | Select and view a customer account
- C4102861 | View and export a customer's Journey History
- C4102862 | View and export a customer's Transaction History
- C4102863 | Queue a refund from a transaction
- C4102867 | View all taps including taps not valid for a journey
- C4102868 | Corrupt tap messages are rejected and quarantined
- C4102869 | Configure a daily capping rule
- C4102870 | Configure weekly and monthly capping rules
- C4102871 | Configure a transfer capping rule
- C4102872 | Add, edit and view a price cap
- C4102873 | Deactivate and archive a capping rule
- C4102874 | Price Rule information icon
- C4102875 | A capping rule's created date-time is not set an hour in the future
- C4102876 | Add a daily capping group
- C4102877 | Add a weekly capping group
- C4102878 | Configure the End of the Operational Day and Week
- C4102879 | Configure the maximum late data period
- C4102880 | Configure the maximum journey duration
- C4102881 | Configure debt-recovery retry attempts and message
- C4102882 | Configure a minimum fare for an e-Purse smartcard
- C4102883 | Run the Account Status Report
- C4102884 | Run the Action List Report
- C4102886 | Run the Aftercare Report
- C4102887 | Run the Audit Report
- C4102888 | Run the Authorisation Failures Report
- C4102889 | Run the Cancelled Tap Report
- C4102890 | Run the Debt Report
- C4102891 | Run the Declined Taps Report
- C4102892 | Run the Deny List Report
- C4102893 | Run the Duplicate Taps Report
- C4102894 | Run the EMV Summary Report
- C4102895 | Run the ePurse Balance Report
- C4102896 | Run the Exception Report
- C4102897 | Run the Expired Tap Report
- C4102898 | Run the Fare Band Report
- C4102899 | Run the Initial Taps by Brand Report
- C4102900 | Run the Inspection Details Report
- C4102901 | Run the Journey Summary Report
- C4102902 | Run the Journeys by Card Scheme Report
- C4102903 | Run the Journeys by Service/Route Report
- C4102904 | Run the Late Taps Report
- C4102905 | Run the Lost Tap Data Report
- C4102906 | Run the PSP Technical Errors Report
- C4102907 | Run the Refunds Report
- C4102908 | Run the Retail Debt Report
- C4102909 | Run the Retail Transactions Report
- C4102910 | Run the Revenue Apportionment Report
- C4102911 | Run the Revenue by Business Rule Report
- C4102912 | Run the Revenue by MID Report
- C4102913 | Run the Revenue Inspection Report
- C4102914 | Run the Shared Liability Report
- C4102915 | Run the Tap Reconciliation Report
- C4102916 | Run the Transaction Report
- C4102917 | Run the Unique Taps Report
- C4102927 | Sign on to an anonymous account
- C4102928 | Sign-on is prevented for invalid, no-journey or blocked cards
- C4102929 | View account balance and home summary
- C4102930 | Sign off the Passenger Web Portal
- C4102931 | View and print Journey History
- C4102932 | View and print Transaction History
- C4102933 | Request a refund
- C4102934 | Retry a declined payment
- C4102935 | Request a card replacement
- C4102936 | Raise a general query
- C4102937 | Declined payments are guaranteed up to the Issuer Liability Threshold
- C4102938 | Account Verification Request on first use of a Visa card
- C4102939 | Pre-Authorisation check on first use each day
- C4102940 | Pre-Authorisation check on first use after removal from the Deny List
- C4102941 | Late taps within the maximum late data period are processed
- C4102942 | Late taps beyond the maximum late data period are rejected
- C4102943 | Capping rules are applied retrospectively to late taps
- C4102944 | Duplicate late taps are disregarded
- C4102953 | Support multiple travel zones for a stop
- C4102954 | Add new decline reasons
- C4102955 | Capping-rule products load from the fares engine

## Title over 72 chars _(advisory)_ - 15
- C4102758 | Correction outside the Metro zone removes the cap and charges the difference - 76 chars
- C4102759 | Correction into the Metro zone applies the cap and refunds the difference - 73 chars
- C4102767 | Re-running settlement after a correction does not re-charge the capped tap - 74 chars
- C4102769 | Higher-fare correction outside the zone removes the cap and charges the difference - 82 chars
- C4102786 | Aligning two different-ref taps to the same ref applies the cap and refunds - 75 chars
- C4102789 | Correction outside the town to a higher fare removes the cap and charges the difference - 87 chars
- C4102793 | Re-tap at the same stage after annulment is the first ref fare tap (Ulsterbus) - 78 chars
- C4102803 | Annulling the first capped-day tap then re-tapping restores correct totals - 74 chars
- C4102809 | A valid tap rejected as duplicate is retained when the first tap is cancelled - 77 chars
- C4102810 | Several same-stage taps then cancelling the first promotes the next valid tap - 77 chars
- C4102812 | Annulment processed before the second tap makes it a normal first journey - 73 chars
- C4102818 | Multiple interleaved retail transactions never reset the duplicate reference - 76 chars
- C4102828 | A cancelled journey stays cancelled after a stop correction and further settlement - 82 chars
- C4102854 | The recovered account is visible in the Operator Portal with the correct status - 79 chars
- C4102855 | Recovery behaviour is observable in the Operator Portal, logging verified by dev tests - 86 chars

## Objective/preface empty - 0
_none_

## Objective not starting 'This test is to confirm' - 0
_none_

## Preconditions empty - 0
_none_

## Preconditions without a GIVEN - 0
_none_

## No When/Then steps at all - 0
_none_

## First step is not a WHEN - 0
_none_

## Step content not WHEN/AND - 0
_none_

## A WHEN with no THEN outcome - 0
_none_

## Genuine compound THEN (two distinct outcomes) - should split - 0
_none_

## Expected (prose) empty - 0
_none_

## Expected starts with THEN (should be prose) - 0
_none_

## Tags (@project/@device/...) written into the case - 0
_none_

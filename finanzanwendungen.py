import streamlit as st
import pandas as pd
import plotly.graph_objs as go

st.sidebar.title('Finanzanwendungen')
app_option = st.sidebar.radio('Wählen Sie eine Anwendung:', ['Sparplanrechner', 'Tilgungsrechner', 'Mieteinnahmenrechner', 'Immobilienwertrechner', 'Auszahlungsplanrechner'])

if app_option == 'Sparplanrechner':
    st.title('Sparplanrechner')

    # Eingabefelder für den Investitionsrechner
    start_kapital = st.number_input("Startkapital eingeben:", min_value=0.0, format="%.2f")
    jaehrliche_rendite = st.number_input("Jährliche Rendite in % eingeben:", min_value=0.0, format="%.2f")
    monatliche_sparrate_vorschuessig = st.number_input("Monatlichen Sparbetrag (vorschüssig) eingeben:", min_value=0.0, format="%.2f")
    anlage_zeitraum = st.number_input("Anlagezeitraum in Jahren eingeben:", min_value=0, step=1, format="%d")
    
    st.divider()
    #--------------------------------------------------------------------#

    # Berechnung und Anzeige des Ergebnisses
    if st.button('Berechnung starten'):
        monatliche_rendite = jaehrliche_rendite / (12 * 100)
        zwischenwert = start_kapital
        zwischenwert_liste = [start_kapital,]
        beitraege_kumuliert = start_kapital
        liste_beitraege_kumuliert = []
        steuern = []
        monatliche_steuer_kumuliert = 0
        nettogewinne = []
        
        for month in range(int(anlage_zeitraum * 12)):
            beitraege_kumuliert = beitraege_kumuliert + monatliche_sparrate_vorschuessig
            liste_beitraege_kumuliert.append(beitraege_kumuliert)
            zwischenwert = (zwischenwert + monatliche_sparrate_vorschuessig) * (1 + monatliche_rendite)
            zwischenwert_liste.append(zwischenwert)
            
            monatliche_steuer_kumuliert = 0.186425 * (zwischenwert - beitraege_kumuliert)
            steuern.append(monatliche_steuer_kumuliert)
            
            monatlicher_nettogewinn = zwischenwert - monatliche_steuer_kumuliert - beitraege_kumuliert
            nettogewinne.append(monatlicher_nettogewinn)
            
            
        gewinn = zwischenwert - beitraege_kumuliert
        steuer = gewinn * 0.186425
        endwert_nettogewinn = zwischenwert * monatliche_rendite * (1-0.186425)
        
        
        #st.write(f'Das Kapital nach {int(anlage_zeitraum)} Jahren beträgt {zwischenwert:,.2f} Euro')
        st.metric(label=f"Endwert nach {int(anlage_zeitraum)} Jahren:", value=f"{zwischenwert:,.2f} €", delta=None)
        
        st.metric(label=f"Endwert bei reinen Aktien-ETFs nach {int(anlage_zeitraum)} Jahren nach Steuern:", value=f"{zwischenwert - steuer:,.2f} €", delta=None)
        
        st.metric(label="Kapitalertragssteuer:", value=f"{steuer:,.2f} €", delta=None)
        
        st.metric(label="Summe aller Beiträge inkl. Startkapital:", value=f"{beitraege_kumuliert:,.2f} €", delta=None)
        
        st.metric(label="Gewinn:", value=f"{gewinn:,.2f} €", delta=None)
        
        st.metric(label="Monatlicher Netto-Gewinn nach Abschluss der Ansparphase:", value=f"{endwert_nettogewinn:,.2f} €", delta=None)
        
        
      
        df = pd.DataFrame({
            "Monat": range(len(steuern)),
            "Netto-Gewinn": nettogewinne,
            "Steueranteil": steuern,
            "Beiträge": liste_beitraege_kumuliert
        })
        
        
        # Erstellen des Plotly-Graphen mit fig_2
        fig = go.Figure()
        
        # Beitragsanteil
        fig.add_trace(go.Bar(
            x=df["Monat"],
            y=df["Beiträge"],
            name="Beiträge",
            marker_color='yellow'
        ))
        
        # Gewinnanteil
        fig.add_trace(go.Bar(
            x=df["Monat"],
            y=df["Netto-Gewinn"],
            name="Netto-Gewinn",
            marker_color='blue'
        ))
        
        # Steueranteil
        fig.add_trace(go.Bar(
            x=df["Monat"],
            y=df["Steueranteil"],
            name="Steueranteil",
            marker_color='red'
        ))
        
        
        # Aktualisieren des Layouts für einen gestapelten Barchart
        fig.update_layout(
            barmode='stack',  # Dies bewirkt, dass die Balken gestapelt werden
            title='Aggregierter Barchart für kumulierte Beiträge, Gewinne und Steuern',
            xaxis_title='Monat',
            yaxis_title='Betrag',
            legend_title='Anteile'
        )
        
        # Anzeigen des Plotly-Graphen in Streamlit
        st.plotly_chart(fig, use_container_width=True)
                
##################################################################################################################################################

elif app_option == 'Tilgungsrechner':
    st.title('Tilgungsrechner')

    # Eingabefelder für den Tilgungsrechner
    restkredit = st.number_input('Kreditsumme eingeben:', min_value=0.0, format="%.2f")
    tilgungsrate_monatlich = st.number_input('Monatliche Annuität (Tilgung + Zins) eingeben:', min_value=0.0, format="%.2f")
    kreditzins = st.number_input('Nominalen Kreditzins (in %) eingeben:', min_value=0.0, format="%.2f")
    zinsbindungsdauer = st.number_input('Zinsbindungsdauer in Jahren eingeben (optional):', min_value=0, format="%.2i")
   
    st.divider()
    #--------------------------------------------------------------------#
    
    
    immowert = st.checkbox('Berechne den Immobilienwert nach Tilgungsende', value=False)
    
    if immowert:
    
        immobilienwert = st.number_input('Immobillienwert eingeben:', min_value=0.0, format="%.2f")
        immobilienrendite = st.number_input('Geschätzte jährliche Preissteigerung der Immobillie in % eingeben:', min_value=0.0, format="%.2f")
    
    st.divider()
    #--------------------------------------------------------------------#

    vermietet = st.checkbox('Berechne die Mieteinnahmen bis Tilgungsende', value=False)
    
    if vermietet:
        kaltmiete = st.number_input('Kaltmiete eingeben:', min_value=0.0, format="%.2f")
        instandhaltungskosten = st.number_input('Monatliche Instandhaltungskosten eingeben:', min_value=0.0, format="%.2f")
        hausgeld = st.number_input('Hausgeld eingeben:', min_value=0.0, format="%.2f")
        mietsteigerung = st.number_input('Geschätzte jährliche Mietsteigerung eingeben:', min_value=0.0, format="%.2f")
        versicherungskosten = st.number_input('Versicherungskosten eingeben:', min_value=0.0, format="%.2f")
        leerstand = st.number_input('Geschätzten Leerstand im Jahr (in Monaten) eingeben:', min_value=0.0, format="%.2f")
        
    st.divider()
    #--------------------------------------------------------------------#
        
    # Berechnen Button
    if st.button('Berechnung starten'):      
        restkredit_nach_tilgung = []  # Restkredit nach Tilgung
        kreditsumme = restkredit

        zinsaufwendungen = []  # monatliche Zinsaufwendungen
        kumulierte_zinsaufwendungen = []  # kumulierte Zinsaufwendungen
        
        tilgungsanteile = []
        kumulierte_tilgungsanteile = []
        
        counter = 0  # zählt die Monate
        erste_zinsaufwendung = restkredit * (kreditzins / (12 * 100))  # erste Zinsaufwendung

        if erste_zinsaufwendung >= tilgungsrate_monatlich:
            st.write(f'Die monatliche Tilgungsrate (derzeit {tilgungsrate_monatlich:,.2f} €) muss größer sein als die erste Zinsaufwendung (derzeit {erste_zinsaufwendung:,.2f} €) !')
        elif restkredit <=0:
            st.write('Es gibt nichts zu tilgen !')
        else:
            while restkredit > 0.0:
                monatliche_zinsaufwendung = restkredit * (kreditzins / (12 * 100))
                zinsaufwendungen.append(monatliche_zinsaufwendung)
                kumulierte_zinsaufwendungen.append(sum(zinsaufwendungen))
                
                if tilgungsrate_monatlich <= restkredit:
                    monatlicher_tilgungsanteil = tilgungsrate_monatlich - monatliche_zinsaufwendung
                else:
                    monatlicher_tilgungsanteil = restkredit 
                
                restkredit -= (tilgungsrate_monatlich - monatliche_zinsaufwendung)
                restkredit = max(restkredit, 0)  # Verhindert negative Restschuld
                restkredit_nach_tilgung.append(restkredit)
                
                
                tilgungsanteile.append(monatlicher_tilgungsanteil)
                kumulierte_tilgungsanteile.append(sum(tilgungsanteile))
                
                counter += 1

            st.write('-' * 20)
            # st.write(f'Die Kreditsumme ist nach {counter} Monaten (oder {counter/12:,.2f} Jahren) abbezahlt !')
            st.metric(label="Vollständige Kredittilgung:", value=f"in {counter} Monaten ({counter//12} Jahre und {counter%12} Monate)" , delta=None)

            # st.write(f'Die Zinslast über die gesamte Laufzeit beträgt {kumulierte_zinsaufwendungen[-1]:,.2f} Euro')
            st.metric(label="Zinsaufwendungen nach vollständiger Kredittilgung:", value=f"{kumulierte_zinsaufwendungen[-1]:,.2f} €   🙈", delta=None)
            
            st.metric(label="Gesamtbelastung nach vollständiger Kredittilgung:", value=f"{kumulierte_zinsaufwendungen[-1] + kreditsumme:,.2f} €   🙉", delta=None)
            
           
          
            
            # Optionale Ausgabe, wenn bereits Berechnungen durchgeführt wurden

            if zinsbindungsdauer == 0:
                pass
            elif zinsbindungsdauer*12 > counter:
                
                st.divider()
                #--------------------------------------------------------------------#
      
                st.write("Die Kreditsumme ist bereits vor Erreichung der Zinsbindungsdauer komplett abbezahlt.")
                #st.metric(label="Zinsanteil nach vollständiger Kredittilgung:", value=f"{kumulierte_zinsaufwendungen[-1]:,.2f} €", delta=None)
            else:
                
                st.divider()
                #--------------------------------------------------------------------#
    
                #st.write(f"Die kumulierten Zinsaufwendungen nach {zinsbindungsdauer} Jahr(en) betragen: {kumulierte_zinsaufwendungen[zinsbindungsdauer*12-1]:,.2f} €")
                st.metric(label="Zinsaufwendungen nach Zinsbindungsdauer:", value=f"{kumulierte_zinsaufwendungen[zinsbindungsdauer*12-1]:,.2f} €", delta=None)
                #st.write(f"Die Restschuld nach {zinsbindungsdauer} Jahr(en) beträgt: {restkredit_nach_tilgung[zinsbindungsdauer*12-1]:,.2f} Euro")
                st.metric(label="Offener Kredit nach Zinsbindungsdauer:", value=f"{restkredit_nach_tilgung[zinsbindungsdauer*12-1]:,.2f} €", delta=None)
                               
           
            if immowert:
                
                st.divider()
                #--------------------------------------------------------------------#
            
                # Immobilienwert nach abzahlung der Kreditsumme
                IeW = immobilienwert*(1+immobilienrendite/100)**(counter/12)
                if IeW == 0:
                    pass
                else:
                    #st.write(f'Der Immobillienwert nach vollständiger Kredittilgung (nach {counter/12:,.2f} Jahren): {IeW:.2f}')
                    st.metric(label="Immobillienwert nach vollständiger Kredittilgung:", value=f"{IeW:,.2f} €", delta=None)


            
            if vermietet:
                
                st.divider()
                #--------------------------------------------------------------------#
                
                # Berechne die Nettomieteinnahmen über die Laufzeit des Kredites           
                nettomiete = kaltmiete - instandhaltungskosten - hausgeld - versicherungskosten - leerstand/12*kaltmiete
                jaehrliche_nettomiete = nettomiete*12
                
                
                tilgungsdauer = counter//12
                mieteinnahmen = 0
                for jahr in range(tilgungsdauer):
                    mieteinnahmen = mieteinnahmen + jaehrliche_nettomiete * (1+mietsteigerung/100)**jahr
                
                st.metric(label="Nettomieteinnahmen nach Ablauf der Tilgungsdauer:", value=f"{mieteinnahmen:,.2f} €", delta=None)
            
            st.divider()
            #--------------------------------------------------------------------#
            
            df_2 = pd.DataFrame({
                "Monat": range(len(kumulierte_tilgungsanteile)),
                "Tilgungsanteil": kumulierte_tilgungsanteile,
                "Zinsanteil": kumulierte_zinsaufwendungen
            })
            
            
            # Erstellen des Plotly-Graphen mit fig_2
            fig_2 = go.Figure()
            
            # Tilgungsanteil
            fig_2.add_trace(go.Bar(
                x=df_2["Monat"],
                y=df_2["Tilgungsanteil"],
                name="Tilgungsanteil",
                marker_color='blue'
            ))
            
            # Zinsanteil
            fig_2.add_trace(go.Bar(
                x=df_2["Monat"],
                y=df_2["Zinsanteil"],
                name="Zinsanteil",
                marker_color='red'
            ))
            
            # Aktualisieren des Layouts für einen gestapelten Barchart
            fig_2.update_layout(
                barmode='stack',  # Dies bewirkt, dass die Balken gestapelt werden
                title='Aggregierter Barchart für kumulierte Tilgungs- und Zinsanteile',
                xaxis_title='Monat',
                yaxis_title='Betrag',
                legend_title='Anteile'
            )
            
            # Anzeigen des Plotly-Graphen in Streamlit
            st.plotly_chart(fig_2, use_container_width=True)
            
            
            st.divider()
            #--------------------------------------------------------------------#
            
            df_3 = pd.DataFrame({
                "Monat": range(len(tilgungsanteile)),
                "Tilgungsanteil": tilgungsanteile,
                "Zinsanteil": zinsaufwendungen
            })
            
            
            # Erstellen des Plotly-Graphen mit fig_2
            fig_3 = go.Figure()
            
            # Tilgungsanteil
            fig_3.add_trace(go.Bar(
                x=df_3["Monat"],
                y=df_3["Tilgungsanteil"],
                name="Tilgungsanteil",
                marker_color='blue'
            ))
            
            # Zinsanteil
            fig_3.add_trace(go.Bar(
                x=df_3["Monat"],
                y=df_3["Zinsanteil"],
                name="Zinsanteil",
                marker_color='red'
            ))
            
            # Aktualisieren des Layouts für einen gestapelten Barchart
            fig_3.update_layout(
                barmode='stack',  # Dies bewirkt, dass die Balken gestapelt werden
                title='Aggregierter Barchart für Tilgungs- und Zinsanteile',
                xaxis_title='Monat',
                yaxis_title='Betrag',
                legend_title='Anteile'
            )
            
            # Anzeigen des Plotly-Graphen in Streamlit
            st.plotly_chart(fig_3, use_container_width=True)
            
            
            annuitaet_liste = [tilgungsrate_monatlich] * (len(restkredit_nach_tilgung) - 1)
            annuitaet_liste.append(restkredit_nach_tilgung[-2] + zinsaufwendungen[-1]) 
            
            df_5 = pd.DataFrame({
                "Monat": range(1, len(restkredit_nach_tilgung) + 1),  # Erzeugt eine Liste von Monaten
                "Annuität": annuitaet_liste ,  # Wiederholt den Wert für jede Zeile
                "Tilgungsanteil": tilgungsanteile,
                "Zinsanteil": zinsaufwendungen,
                "Tilgung (kumuliert)": kumulierte_tilgungsanteile,              
                "Zinsen (kumuliert)": kumulierte_zinsaufwendungen,
                "Restsumme": restkredit_nach_tilgung
                })
            
            df_5.set_index("Monat", inplace=True)
            
            df_styled = df_5.style.format({
                "Restsumme": "{:,.2f} €",
                "Annuität": "{:,.2f} €",
                "Tilgungsanteil": "{:,.2f} €",
                "Tilgung (kumuliert)": "{:,.2f} €",
                "Zinsanteil": "{:,.2f} €",
                "Zinsen (kumuliert)": "{:,.2f} €"
                })


            # Anzeigen der Tabelle in der Streamlit App
            st.dataframe(df_styled)
            
##################################################################################################################################################


elif app_option == 'Mieteinnahmenrechner':
    st.title('Mieteinnahmenrechner')          
    
    kaltmiete = st.number_input('Kaltmiete eingeben:', min_value=0.0, format="%.2f")
    instandhaltungskosten = st.number_input('Monatliche Instandhaltungskosten eingeben:', min_value=0.0, format="%.2f")
    hausgeld = st.number_input('Hausgeld eingeben:', min_value=0.0, format="%.2f")
    versicherungskosten = st.number_input('Versicherungskosten eingeben:', min_value=0.0, format="%.2f")
    leerstand = st.number_input('Geschätzten Leerstand im Jahr (in Monaten) eingeben:', min_value=0.0, format="%.2f")
    mietdauer = st.number_input('Mietdauer (in Jahren) eingeben:', min_value=0, step=1, format="%d")
    mietsteigerung = st.number_input('Geschätzte jährliche Netto-Mietsteigerung (in %) eingeben:', min_value=0.0, format="%.2f")
    
    nettomiete = kaltmiete - instandhaltungskosten - hausgeld - versicherungskosten - leerstand/12*kaltmiete
    jaehrliche_nettomiete = nettomiete*12
    
    st.divider()
    #--------------------------------------------------------------------#
    
    if st.button('Berechnung starten'):      
   
        mieteinnahmen = 0
        for jahr in range(mietdauer):
            mieteinnahmen = mieteinnahmen + jaehrliche_nettomiete * (1+mietsteigerung/100)**jahr
        
        st.metric(label=f"Nettomieteinnahmen nach {mietdauer} Jahren:", value=f"{mieteinnahmen:,.2f} €", delta=None)
        
##################################################################################################################################################

        
elif app_option == 'Immobilienwertrechner':
     st.title('Immobilienwertrechner')
     
     immobilienwert = st.number_input('Immobillienwert eingeben:', min_value=0.0, format="%.2f")
     immobilienrendite = st.number_input('Geschätzte jährliche Preissteigerung der Immobillie (in %) eingeben:', min_value=0.0, format="%.2f")
     
     haltedauer = st.number_input('Haltedauer (in Jahren) eingeben:', min_value=0, step=1, format="%d")
     
     st.divider()
     #--------------------------------------------------------------------#
     
     if st.button('Berechnung starten'):      
    
        # Immobilienwert nach abzahlung der Kreditsumme
        IeW = immobilienwert*(1+immobilienrendite/100)**(haltedauer)

        #st.write(f'Der Immobillienwert nach vollständiger Kredittilgung (nach {counter/12:,.2f} Jahren): {IeW:.2f}')
        st.metric(label=f"Immobillienwert nach {haltedauer} Jahren:", value=f"{IeW:,.2f} €", delta=None)
        
##################################################################################################################################################

elif app_option == 'Auszahlungsplanrechner':
    st.title('Auszahlungsplanrechner')        
        
    start_kapital = st.number_input('Startkapital eingeben:', min_value=0.0, format="%.2f")
    
    erwartete_rendite = st.number_input('Jährliche Rendite (in %) eingeben:', min_value=0.0, format="%.2f")  
    
    monatliche_auszahlung = st.number_input('Monatliche Auzahlung eingeben:', min_value=0.0, format="%.2f") 
    
    st.divider()
    #--------------------------------------------------------------------#
    
    if st.button('Berechnung starten'):    
    
        rest_kapital = start_kapital
        monat = 0
        erste_monatliche_rendite = start_kapital * (erwartete_rendite/(12*100))
        
        daten = []
            
        if erste_monatliche_rendite > monatliche_auszahlung:
            st.write(f'Die monatliche Auszahlung muss die monatliche Rendite ({erste_monatliche_rendite:.2f} €) übersteigen.')
        else:  
            while rest_kapital > monatliche_auszahlung:      
                
                monatliche_rendite = rest_kapital * (erwartete_rendite/(12*100))
               
                rest_kapital = rest_kapital * (1+erwartete_rendite/(12*100)) - monatliche_auszahlung
                
                monat += 1
                
                daten.append([monat, monatliche_auszahlung, monatliche_rendite, rest_kapital])
        
        
        st.write(f'Das Kapital ist nach {monat // 12} Jahren und {monat % 12} Monaten aufgebraucht')
        
        
        df_6 = pd.DataFrame(daten, columns=['Monat', 'Monatliche Auszahlung', 'Monatliche Rendite', 'Restkapital'])

        df_6.set_index("Monat", inplace=True)   
        
        # Konvertieren der Werte in Euro-Format, außer der ersten Spalte (Monat)
        df_6['Monatliche Auszahlung'] = df_6['Monatliche Auszahlung'].apply(lambda x: f"{x:,.2f} €")
        df_6['Monatliche Rendite'] = df_6['Monatliche Rendite'].apply(lambda x: f"{x:,.2f} €")
        df_6['Restkapital'] = df_6['Restkapital'].apply(lambda x: f"{x:,.2f} €")
        

        # Anzeige des DataFrames
        st.write(df_6)
    



��    0      �  C         (     )     0     <     Q     f     �  %   �     �  p   �  &   F     m     ~     �     �     �     �     �                 %   6     \     j     {     �  #   �     �  +   �  ,     *   H  )   s     �     �     �     �     �  �  �  ;   �  *   �  /     �   O  (     �   1     �  )   �  )     
   I  j  T     �     �     �     �  $        '  /   >     n     �  1        6     G     Y  "   j     �  !   �     �     �     �     �  +        9     I     Z  !   v  .   �  (   �  6   �  6   '  ;   ^  +   �     �     �     �  @   �     $  v  5  1   �  <   �  A     �   ]  +   <  �   h     .  7   G  4        �        +           !      $   #   .         '   0           	         )                        ,         "      &           /                %      *                     (                    -             
                                   Cancel Client stop Connected to broker. Connecting to broker Could not decode command: Disconnected from broker! Error try install paho-mqtt manually. First station number Having a shared MQTT client simplifies configuration and lowers overhead on the OSPy process, network and broker Leave blank to not publish OSPy status MQTT Broker Host MQTT Broker Password MQTT Broker Port MQTT Broker Username MQTT Client ID MQTT Plugin requires paho mqtt. MQTT Publish up/down topic MQTT client MQTT plug-in MQTT plug-in is disabled. MQTT plugin couldnot initalize client MQTT settings Message received PIP is not installed. Paho-mqtt is not installed. Please wait installing paho-mqtt... Please wait installing pip... Required to receive and send MQTT messages. Required to receive secondary MQTT messages. Skipping command, rain delay is activated! Skipping command, rain sense is detected! Station count Status Submit Subscribe topic Subscribing to topic The mqtt_secondary plugin allows multiple secondary OSPy controlers to be running with the control OSPy system running. This means that one OSPy system can act as the control driver for secondary systems that also use OSPy and have the mqtt_secondary plugin installed. The control OSPy sends a list containing the on/off states of all stations. The secondary system receives the list and checks whether it is necessary to switch on one of its stations or switch it off and make the necessary changes. All irrigation plans are set on the main system and it records all running stations as if they were on the OSPy control system itself. There is no feedback from the secondary  OSPy, so the control system assumes that all stations are working as they should. If enabled logging in secondary OSPy, stations running on this secondary OSPy are also stored in the log. This provides a way to check if the station on the secondary is working properly. Requirements: This plugin requires the main OSPy control system, which has the basic mqtt plugin and the mqtt_zones plugin installed. Each secondary OSPy system must have the basic mqtt plugin installed. You must this OSPy switch to manual mode! If you change settings you must restarting OSPy! The number from the master of this secondary first station. The number of station this secondary uses. The topic to subscribe to for control commands. This MQTT plugin adds an MQTT client to the OSPy daemon for other plugins to use to publish information and or receive commands over MQTT. On this page, the shared client is configured This operation takes longer (minutes)... This plugin needs paho-mqtt. If not installed paho-mqtt, plugin installs paho-mqtt in to the system himself. On first use (if run installation paho-mqtt) please wait for status Use MQTT secondary We can use a public Broker server to test You must this OSPy switch to manual mode! Zone topic Project-Id-Version: 
PO-Revision-Date: 2020-07-03 07:40+0200
Language-Team: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Generated-By: pygettext.py 1.5
X-Generator: Poedit 2.3.1
Last-Translator: Martin Pihrt <martinpihrt@gmail.com>
Plural-Forms: nplurals=3; plural=(n==1 ? 0 : n>=2 && n<=4 ? 1 : 2);
Language: sk_SK
 Zrušiť Klient stop Pripojenie k maklérovi. Pripojenie k Brokeru MQTT nedokázal dekódovať príkaz: Odpojené od makléra! Chyba skúste: pip install paho-mqtt manuálne. Číslo prvej stanice S zdieľaným klientom MQTT zjednodušuje konfiguráciu a znižuje režijné náklady na proces OSPy, sieť a makléra (Broker) Ponechajte prázdne, aby sa nezverejnil stav OSPy MQTT Broker Host MQTT Broker heslo MQTT Broker Port MQTT Broker používateľské meno ID klienta MQTT Doplnok MQTT vyžaduje paho mqtt. MQTT Publikujte tému UP/DOWN Klient MQTT MQTT doplnok Doplnok je zakázaný. Doplnok MQTT nemohol inicializovať klienta Nastavenia MQTT Prijatá správa PIP nie je nainštalovaný. Paho-mqtt nie je nainštalovaný. Počkajte prosím na inštaláciu paho-mqtt... Počkajte, prosím, inštalácia pip.... Vyžaduje sa na prijímanie a odosielanie správ MQTT. Vyžaduje sa na prijímanie sekundárnych správ MQTT. Preskakuje sa príkaz,, oneskorenie dažďa je aktivované! Preskakuje sa príkaz, detekuje sa dážď! Počet staníc Stav Odoslať Téma, ktorá sa má prihlásiť na odber ovládacích príkazov Odoberanie témy Doplnok mqtt_secondary umožňuje spustenie viacerých sekundárnych ospy controlorov s ovládacím systémom OSPy. To znamená, že jeden systém OSPy môže pôsobiť ako ovládač ovládacieho prvku pre sekundárne systémy, ktoré tiež používajú OSPy a majú nainštalovaný doplnok mqtt_secondary. Ovládací systém OSPy odošle zoznam obsahujúci stavy zapnutia/vypnutia všetkých staníc. Sekundárny systém prijíma zoznam a skontroluje, či je potrebné zapnúť jednu zo svojich staníc alebo ho vypnúť a vykonať potrebné zmeny. Všetky zavlažovacie plány sú nastavené na hlavnom systéme a zaznamenáva všetky bežecké stanice, ako keby boli na samotnom systéme riadenia OSPy. Neexistuje žiadna spätná väzba od sekundárneho OSPy, takže riadiaci systém predpokladá, že všetky stanice pracujú tak, ako by mali. Ak je povolené zapisovanie do denníka v sekundárnom OSPy, stanice spustené na tomto sekundárnom OSPy sú tiež uložené v denníku. To poskytuje spôsob, ako skontrolovať, či stanica na sekundárne pracuje správne. Požiadavky: Tento plugin vyžaduje hlavný systém riadenia OSPy, ktorý má základné mqtt plugin a mqtt_zones plugin nainštalovaný. Každý sekundárny systém OSPy musí mať nainštalovaný základný modul mqtt. Musíte tento OSPy prepnúť do manuálneho režimu! Ak zmeníte nastavenia, musíte reštartovať OSPy! Číslo majstra tejto sekundárnej prvej stanice. Počet staníc, ktoré toto sekundárne použitie používa. Téma, ktorá sa má prihlásiť na odber ovládacích príkazov. Tento doplnok MQTT pridáva do klienta MQTT ako démona v OSPy ďalšie doplnky, ktoré sa používajú na publikovanie informácií a prijímanie príkazov cez MQTT. Na tejto stránke je nakonfigurovaný zdieľaný klient Táto operácia trvá dlhšie (minúty) ... Tento doplnok potrebuje paho-mqtt. Ak nie je nainštalovaný paho-mqtt, nainštaluje doplnok paho-mqtt do systému sám. Pri prvom použití (ak spustíte inštaláciu paho-mqtt) čakajte na koniec Použit sekundárne MQTT Na otestovanie môžeme použiť verejný server Broker Tento OSPy musíte prepnúť do manuálneho režimu! Téma pre zóny 
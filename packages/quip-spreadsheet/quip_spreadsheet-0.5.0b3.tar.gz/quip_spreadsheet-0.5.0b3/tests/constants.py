QUIP_ACCESS_TOKEN = "1ee2demdo33=|03e39j94r4|komes234mfmf+wapdmeodmemdfg2y6hMfAHko=" # This is a fake token :D
QUIP_BASE_URL = "https://platform.quip.com"
ENV = "DEBUG"
LOGS_PREFIX = ":quip.quip:"
USER_JSON = {
    "name": "John Doe",
    "id": "1234",
    "is_robot": False,
    "affinity": 0.0,
    "desktop_folder_id": "abc1234",
    "archive_folder_id": "abc5678",
    "starred_folder_id": "abc9101",
    "private_folder_id": "abc1121",
    "trash_folder_id": "abc3141",
    "shared_folder_ids": ["abc5161", "abc7181"],
    "group_folder_ids": ["abc9202", "abc1222"],
    "profile_picture_url": f"{QUIP_BASE_URL}/pic.jpg",
    "subdomain": None,
    "url": QUIP_BASE_URL,
}
FOLDER_JSON = {
    "children": [{"thread_id": "abc7181"}, {"folder_id": "abc5161"}],
    "folder": {
        "created_usec": 1606998498297926,
        "creator_id": "1234",
        "id": "abc9101",
        "title": "Starred",
        "updated_usec": 1609328575547507,
    },
    "member_ids": ["1234"],
}
THREAD_JSON = {
    "access_levels": {
        "1234": {"access_level": "OWN"},
    },
    "expanded_user_ids": ["1234"],
    "thread": {
        "author_id": "1234",
        "thread_class": "document",
        "id": "567mnb",
        "created_usec": 1608114559763651,
        "updated_usec": 1609261609357637,
        "link": f"{QUIP_BASE_URL}/abcdefg12345",
        "type": "spreadsheet",
        "title": "My Spreadsheet",
        "document_id": "9876poiu",
        "is_deleted": False,
    },
    "user_ids": [],
    "shared_folder_ids": ["abc1234"],
    "invited_user_emails": [],
    "html": "<h1 id='9876poiu'>My Spreadsheet</h1>",
}
SPREADSHEET_CONTENT = """<h1 id='9876poiu'>My Spreadsheet</h1>
<div data-section-style='13'>
  <table id='Aec9CAvyP44' title='Sheet1' style='width: 237.721em'>
    <thead>
      <tr>
        <th class='empty' style='width: 2em'/>
        <th id='Aec9CAACdyH' class='empty' style='width: 1.8em'>A<br/></th>
        <th id='Aec9CAH7YBR' class='empty' style='width: 7.46667em'>B<br/></th>
        <th id='Aec9CAwvN9F' class='empty' style='width: 19.9333em'>C<br/></th>
        <th id='Aec9CAe1yQ0' class='empty' style='width: 6.71634em'>D<br/></th>
        <th id='Aec9CAAIaj1' class='empty' style='width: 6em'>T<br/></th>
        <th id='Aec9CAWcoFU' class='empty' style='width: 6em'>U<br/></th>
        <th id='Aec9CAkrCad' class='empty' style='width: 6em'>V<br/></th>
      </tr>
    </thead>
    <tbody>
      <tr id='Aec9CAmLjDE'>
        <td style='background-color:#f0f0f0'>1</td>
        <td id='s:Aec9CAmLjDE_Aec9CA0oPBj' style='background-color:#FFDF99;' class='bold'>
          <span id='s:Aec9CAmLjDE_Aec9CA0oPBj'>TECH TRACK</span>
          <br/>
        </td>
        <td id='s:Aec9CAmLjDE_Aec9CAWFNOe' style=''>
          <span id='s:Aec9CAmLjDE_Aec9CAWFNOe'>\u200b</span>
          <br/>
        </td>
        <td id='s:Aec9CAmLjDE_Aec9CAHOMxq' style=''>
          <span id='s:Aec9CAmLjDE_Aec9CAHOMxq'>\u200b</span>
          <br/>
        </td>
        <td id='s:Aec9CAmLjDE_Aec9CAf7d0s' style=''>
          <span id='s:Aec9CAmLjDE_Aec9CAf7d0s'>\u200b</span>
          <br/>
        </td>
        <td id='s:Aec9CAmLjDE_Aec9CAEwmwC' style=''>
          <span id='s:Aec9CAmLjDE_Aec9CAEwmwC'>\u200b</span>
          <br/>
        </td>
        <td id='s:Aec9CAmLjDE_Aec9CA0lijP' style=''>
          <span id='s:Aec9CAmLjDE_Aec9CA0lijP'>\u200b</span>
          <br/>
        </td>
        <td id='s:Aec9CAmLjDE_Aec9CA003da' style=''>
          <span id='s:Aec9CAmLjDE_Aec9CA0lijP'>\u200b</span>
          <br/>
        </td>
      </tr>
      <tr id='Aec9CAITZFz'>
        <td style='background-color:#f0f0f0'>2</td>
        <td id='s:Aec9CAITZFz_Aec9CA0oPBj' style='background-color:#FFDF99;' class='bold'>
          <span id='s:Aec9CAITZFz_Aec9CA0oPBj'>\u200b</span>
          <br/>
        </td>
        <td id='s:Aec9CAITZFz_Aec9CAWFNOe' style='background-color:#FFDF99;' class='bold'>
          <span id='s:Aec9CAITZFz_Aec9CAWFNOe'>Date</span>
          <br/>
        </td>
        <td id='s:Aec9CAITZFz_Aec9CAHOMxq' style='background-color:#FFDF99;' class='bold'>
          <span id='s:Aec9CAITZFz_Aec9CAHOMxq'>Title</span>
          <br/>
        </td>
        <td id='s:Aec9CAITZFz_Aec9CAf7d0s' style='background-color:#FFDF99;' class='bold'>
          <span id='s:Aec9CAITZFz_Aec9CAf7d0s'>Location</span>
          <br/>
        </td>
        <td id='s:Aec9CAITZFz_Aec9CAwdFrL' style='background-color:#FFDF99;' class='bold'>
          <span id='s:Aec9CAITZFz_Aec9CAwdFrL'>Language</span>
          <br/>
        </td>
        <td id='s:Aec9CAITZFz_Aec9CAEwmwC' style='background-color:#FFDF99;' class='bold'>
          <span id='s:Aec9CAITZFz_Aec9CAEwmwC'>Capacity</span>
          <br/>
        </td>
        <td id='s:Aec9CAITZFz_Aec9CA0lijP' style='background-color:#FFDF99;' class='bold'>
          <span id='s:Aec9CAITZFz_Aec9CA0lijP'>Owner</span>
          <br/>
        </td>
      </tr>
      <tr id='Aec9CADeBjI'>
        <td style='background-color:#f0f0f0'>3</td>
        <td id='s:Aec9CADeBjI_Aec9CA0oPBj' style='background-color:#AFEFA9;'>
          <span id='s:Aec9CADeBjI_Aec9CA0oPBj'>\u200b</span>
          <br/>
        </td>
        <td id='s:Aec9CADeBjI_Aec9CAWFNOe' style=''>
          <span id='s:Aec9CADeBjI_Aec9CAWFNOe'>Date</span>
          <br/>
        </td>
        <td id='s:Aec9CADeBjI_Aec9CAHOMxq' style=''>
          <span id='s:Aec9CADeBjI_Aec9CAHOMxq'>Intro to ML on AWS</span>
          <br/>
        </td>
        <td id='s:Aec9CADeBjI_Aec9CAf7d0s' style=''>
          <span id='s:Aec9CADeBjI_Aec9CAf7d0s'>Virtual (Chime)</span>
          <br/>
        </td>
        <td id='s:Aec9CADeBjI_Aec9CAwdFrL' style=''>
          <span id='s:Aec9CADeBjI_Aec9CAwdFrL'>ES</span>
          <br/>
        </td>
        <td id='s:Aec9CADeBjI_Aec9CAEwmwC' style=''>
          <span id='s:Aec9CADeBjI_Aec9CAEwmwC'>50</span>
          <br/>
        </td>
        <td id='s:Aec9CADeBjI_Aec9CA0lijP' style=''>
          <span id='s:Aec9CADeBjI_Aec9CA0lijP'>John Doe</span>
          <br/>
        </td>
      </tr>
    </tbody>
  </table>
</div>"""

package thesonid.com.brailler;

/**
 * Created by Konstantinos Barmpas.
 */

import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;


public class Passwordchange extends AppCompatActivity {

    //Declare Activity variables.

    private EditText passwordedit, boardedit, newpass;
    private Button change;

    /*Gets the data from the TextEdit fields. Does the neccesary data validation.
      Connects to the database.
      If the input password and board number match with a pair of the database then
      it changes the password for that board and return to the MainActivtyBraille. Otherwise
      it shows error message.
    */

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.password_change);
        getSupportActionBar().setDisplayHomeAsUpEnabled(true);

        //Set the EditText areas and buttons of the layout.

        boardedit = (EditText) findViewById(R.id.board_number_password);
        passwordedit = (EditText) findViewById(R.id.old_password);
        newpass = (EditText) findViewById(R.id.new_password);
        change = (Button) findViewById(R.id.change_btn);
        change.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Change();
            }
        });
    }

    private void Change() {

        //Data get and validation
        final String password = passwordedit.getText().toString().trim();
        final String board = boardedit.getText().toString().trim();
        final String newpassword = newpass.getText().toString().trim();

        final DatabaseReference mDatabase;
        mDatabase = FirebaseDatabase.getInstance().getReference();
        DatabaseReference boards = mDatabase.child("Boards");

        if (TextUtils.isEmpty(board)) {
            Toast.makeText(getApplicationContext(), "Please enter board number", Toast.LENGTH_SHORT).show();
            return;
        }
        if (TextUtils.isEmpty(password)) {
            Toast.makeText(getApplicationContext(), "Please enter old password", Toast.LENGTH_SHORT).show();
            return;
        }
        if (TextUtils.isEmpty(newpassword)) {
            Toast.makeText(getApplicationContext(), "Please enter new password", Toast.LENGTH_SHORT).show();
            return;
        }

        //Communication with the database
        final DatabaseReference boardref = boards.child(board).child("password");
        boardref.addListenerForSingleValueEvent(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot snapshot) {
                if (snapshot.hasChild(password)) {
                    boardref.child(newpassword).setValue(newpassword);
                    boardref.child(password).removeValue();
                    Toast.makeText(Passwordchange.this, "Password changed successfully", Toast.LENGTH_LONG).show();
                    finish();
                } else {
                    Toast.makeText(Passwordchange.this, "Board and old password dont match", Toast.LENGTH_LONG).show();
                }
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
            }
        });
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                finish();
                return true;
            default:
                return super.onOptionsItemSelected(item);

        }
    }

}
